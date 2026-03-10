from rest_framework import status, exceptions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from notify.models import ActivityLog

class UpdateModelViewSet(ModelViewSet):
    delete_message = "Object Successfully Deleted!"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return self.perform_retrieve(serializer)
    
    def perform_retrieve(self, serializer):
        return Response(
            {
                'status': True,
                'data': serializer.data
            }, status=status.HTTP_200_OK
        )
    
    def list(self, request, *args, **kwargs):
        try:
            response = super().list(request, *args, **kwargs)
            return Response(
                {
                    'status': True,
                    'count': len(response.data),
                    'data': response.data
                }, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    'status': False,
                    'messgae': str(e),
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(
                {
                    'status': True,
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED
            )
        except exceptions.ValidationError:
            error = {key: str(value[0]) for key, value in serializer.errors.items()}
            return Response(
                {
                    'status': False,
                    'message': error,
                },status=status.HTTP_400_BAD_REQUEST
            )
        except exceptions.PermissionDenied as e:
            return Response(
                {
                    'status': False,
                    'message': str(e),
                }, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    'status': False,
                    'message': str(e),
                }, status=status.HTTP_400_BAD_REQUEST
            )
    
    def update(self, request, *args, **kwargs):
        try:
            object = self.get_object()
            serializer = self.get_serializer(object, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(
                {
                    'status': True,
                    'data': serializer.data
                },
                status=status.HTTP_200_OK
            )
        except exceptions.ValidationError:
            error = {key: str(value[0]) for key, value in serializer.errors.items()}
            return Response(
                {
                    'status': False,
                    'message': error
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response(
            {
                'status': True,
                'message': self.delete_message,
            }, status=status.HTTP_200_OK
        )

class UpdateReadOnlyModelViewSet(ReadOnlyModelViewSet):
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return self.perform_retrieve(serializer)
    
    def perform_retrieve(self, serializer):
        return Response(
            {
                'status': True,
                'data': serializer.data
            }, status=status.HTTP_200_OK
        )
    
    def list(self, request, *args, **kwargs):
        try:
            response = super().list(request, *args, **kwargs)
            return Response(
                {
                    'status': True,
                    'count': len(response.data),
                    'data': response.data
                }, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    'status': False,
                    'messgae': str(e),
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


