from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework.views import View
from django.views import View as django_view
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import urllib.parse
import os
from dotenv import load_dotenv
load_dotenv()
import requests

class HomePage(View):
    def get(self, request):
        return render(request, "home.html")



META_APP_ID = os.getenv("META_APP_ID")
META_APP_SECRET = os.getenv("META_APP_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

class ConnectWhatsapp(View):
    def get(self, request):
        scope = "business_management,whatsapp_business_management,whatsapp_business_messaging"
        oauth_url = (
            "https://www.facebook.com/v18.0/dialog/oauth?"
            + urllib.parse.urlencode({
                "client_id": META_APP_ID,
                "redirect_uri": REDIRECT_URI,
                "scope": scope,
                "response_type": "code"
            })
        )

        return JsonResponse({
            "connect_url": oauth_url
        })


class WhatsappCallbackView(View):
    def exchange_code_for_token(self, code):
        url = "https://graph.facebook.com/v18.0/oauth/access_token"
        params = {
            "client_id": META_APP_ID,
            "client_secret": META_APP_SECRET,
            "redirect_uri": REDIRECT_URI,
            "code": code
        }
        response = requests.get(url, params=params)
        return response.json()

    def get_user_businesses(self, access_token):
        url = "https://graph.facebook.com/v18.0/me?fields=id,name,accounts,businesses&access_token=" + access_token
        resp = requests.get(url)
        return resp.json().get("businesses", {}).get("data", [])

    def get_whatsapp_accounts_for_business(self, business_id, access_token):
        url = f"https://graph.facebook.com/v18.0/{business_id}"
        params = {
            "fields": "owned_whatsapp_business_accounts",
            "access_token": access_token
        }
        resp = requests.get(url, params=params)
        return resp.json()
    
    def get_phone_numbers(self, waba_id, access_token):
        url = f"https://graph.facebook.com/v18.0/{waba_id}/phone_numbers"
        params = {"access_token": access_token}
        resp = requests.get(url, params=params)
        return resp.json().get("data", [])

    def get(self, request, *args, **kwargs):
        code = request.GET.get("code")
        if not code:
            return JsonResponse({"error": "No auth code"}, status=400)

        token_data = self.exchange_code_for_token(code)

        access_token = token_data.get("access_token")
        if not access_token:
            return JsonResponse({"error": "Token exchange failed"}, status=400)

        businesses = self.get_user_businesses(access_token)
        if not businesses:
            return JsonResponse({"error": "No businesses found"}, status=400)
        business = businesses[0]
        business_id = business["id"]

        waba_data = self.get_whatsapp_accounts_for_business(business_id, access_token)
        if not waba_data:
            return JsonResponse({"error": "No Whatsapp business accont found"}, status=400)
        waba_id = waba_data.get("owned_whatsapp_business_accounts", {}).get("data", [])[0].get("id")
        waba_name = waba_data.get("owned_whatsapp_business_accounts", {}).get("data", [])[0].get("name")

        phones = self.get_phone_numbers(waba_id, access_token)
        phone_number = phones[0].get("display_phone_number")
        phone_number_id = phones[0].get("id")
        to_number = "+8801533125837"

        send_message_in_whatsapp = self.send_whatsapp_message(access_token, phone_number_id, to_number, "Test Message")
        print("send_message_in_whatsapp: ", send_message_in_whatsapp)

        return JsonResponse({
            "status": "connected",
            "business_id": business_id,
            "waba_id": waba_id,
            "waba_name": waba_name,
            "phones": phone_number
        })
    
    def send_whatsapp_message(self, access_token, phone_number_id, to_number, message_text):
        url = f"https://graph.facebook.com/v18.0/{phone_number_id}/messages"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        # for last message received before 24 hours, then can use text type otherwise need to use template type
        payload = {
            "messaging_product": "whatsapp",
            "to": to_number,
            "type": "text",
            "text": {
                "body": message_text
            },
            # "type": "template",
            # "template": {
            #     "name": "hello_world",
            #     "language": {"code": "en_US"}
            # }
        }

        response = requests.post(url, json=payload, headers=headers)
        return response.json()


@method_decorator(csrf_exempt, name="dispatch")
class WebhookWhatsapp(View):
    VERIFY_TOKEN = "my_super_secret_token"
    def get(self, request, *args, **kwagrs):
        try:
            mode = request.GET.get("hub.mode")
            token = request.GET.get("hub.verify_token")
            challenge = request.GET.get("hub.challenge")

            if mode == "subscribe" and token == self.VERIFY_TOKEN:
                print("Webhook verified successfully")
                return JsonResponse(int(challenge), safe=False)

            return JsonResponse("Invalid verification token", safe=False, status=403)

        except Exception as e:
            return JsonResponse(str(e), safe=False, status=500)
    
    def post(self, request, *args, **kwagrs):
        try:
            payload = json.loads(request.body) or request.data
            print("Incoming WhatsApp payload:", payload)
            return JsonResponse({"status": "EVENT_RECEIVED"})
        except Exception as e:
            print("Webhook error:", str(e))
            return JsonResponse({"error": str(e)}, status=500)


class PrivacyPolicyView(django_view):
    def get(self, request):
        return render(request, "privacy-policy.html")

