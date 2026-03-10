from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView
from lead_automation.utils import LogActivityModule
from rest_framework.exceptions import ValidationError
from core.choice_select import ACTIVITY_LOG_ACTION_TYPE, PROFILE_STATUS
from django.db import transaction
from rest_framework.permissions import IsAuthenticated

# =================================================================
# Business Client/Member Login Start===========================
class RegisterView(APIView):
    def post(self, request):
        try:
            serializer = UserRegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                serializer.save()
                return Response(
                    {
                        "success": True,
                        "message": "Registration Success!"
                    }, status=status.HTTP_201_CREATED
                )
        except ValidationError:
            print("----------------------------------------")
            error = {kay: str(value[0]) for kay, value in serializer.errors.items()}
            return Response(
                {
                    "success": False,
                    "message": error
                }, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class LoginTokenView(TokenObtainPairView):
    serializer_class = LoginTokenSerializer

    def create_log(self, user, action, entity, metadata={}):
        # user, action, entity, metadata, request
        data = {
            "user": user,
            "action": action,
            "entity": entity,
            "request": self.request,
            "metadata": {"login_method": "password"}
        }
        log = LogActivityModule(data)
        log.create()

    def post(self, request: Request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.get_user()
            if not user.memberships:
                raise Exception("Your profile is block or deleted!")
            if user.memberships.status == PROFILE_STATUS.INACTIVE:
                raise Exception("Your profile is inactive!")
            
            self.create_log(user, ACTIVITY_LOG_ACTION_TYPE.LOGIN, user)

            data = serializer.validated_data
            data["role"] = user.memberships.role
            print("data: ", data)
            return Response(
                {
                    "status": True,
                    "data": data
                }, status=status.HTTP_200_OK
            )
        except ValidationError:
            error = {kay: str(value[0]) for kay, value in serializer.errors.items()}
            return Response(
                {
                    "status": False,
                    "message": error
                }
            )
        except Exception as e:
            return Response(
                {
                    "status": False,
                    "message": str(e)
                }, status=status.HTTP_400_BAD_REQUEST
            )

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserProfileSerializer(instance=user.memberships)
        return Response(
            {
                "success": True,
                "data": serializer.data
            }
        )

# Business Client/Member Login End===========================
# =================================================================



