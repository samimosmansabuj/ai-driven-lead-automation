import requests
from core.choice_select import APP_TITLE

class ConnectedAppWithToken:
    def __init__(self, token_type, token, app_object):
        self.token = token
        self.app_object = app_object
        self.token_type = token_type
    
    def get_connect(self):
        if self.app_object.app_title == APP_TITLE.WHATSAPP_CLOUD:
            whatsapp_cloud = ConnectWhatsapp(self.token_type, self.token, self.app_object)
            return whatsapp_cloud.connected()
        raise Exception("Please use existing app!")


        


class ConnectWhatsapp:
    def __init__(self, token_type, token, app_object):
        self.token = token
        self.token_type = token_type
        self.app_object = app_object

        if self.token_type == "access_code":
            self.access_token_json = self.exchange_code_for_token()
            self.get_access_token = self.access_token_json.get("access_token")
        elif self.token_type == "access_token":
            self.get_access_token = token
            self.access_token_json = {
                'access_token': self.get_access_token,
                'token_type': 'bearer'
            }
    
    def exchange_code_for_token(self):
        url = "https://graph.facebook.com/v23.0/oauth/access_token"
        redirect_url = self.app_object.config.get("redirect_url")
        params = {
            "client_id": self.app_object.app_id,
            "client_secret": self.app_object.app_secret,
            "redirect_uri": redirect_url,
            "code": self.token
        }
        response = requests.get(url, params=params)
        token_data = response.json()
        if not token_data.get("access_token"):
            raise Exception("Token exchange failed")
        return token_data

    def get_information_for_business(self):
        try:
            url = "https://graph.facebook.com/v23.0/me?fields=businesses{owned_whatsapp_business_accounts}&access_token=" + self.get_access_token
            resp = requests.get(url)
            return resp.json().get("businesses", {}).get("data", [])[0]
        except Exception as e:
            raise Exception(str(e))
    
    def get_phone_numbers(self, waba_id):
        url = f"https://graph.facebook.com/v18.0/{waba_id}/phone_numbers"
        params = {"access_token": self.get_access_token}
        resp = requests.get(url, params=params)
        data = resp.json().get("data", [])
        if not data:
            raise Exception("No phone number found")
        return data[0]

    def connected(self):
        information_for_business = self.get_information_for_business()
        business_id = information_for_business.get("id")
        waba_data = information_for_business.get("owned_whatsapp_business_accounts", {}).get("data", [])[0]

        waba_id = waba_data.get("id")
        waba_name = waba_data.get("name")
        phones = self.get_phone_numbers(waba_id)
        # {
        #     'verified_name': 'Test Number',
        #     'code_verification_status': 'NOT_VERIFIED',
        #     'display_phone_number': '15551547561',
        #     'quality_rating': 'GREEN',
        #     'platform_type': 'CLOUD_API',
        #     'throughput': {'level': 'STANDARD'},
        #     'webhook_configuration': {'application': 'https://s3x54djx-8080.inc1.devtunnels.ms/webhook/whatsapp/'},
        #     'id': '907695169103284'
        # }
        
        phone_number = phones.get("display_phone_number")
        phone_number_id = phones.get("id")

        # to_number = "+8801533125837"
        return {
            "status": "connected",
            "business_id": business_id,
            "waba_id": waba_id,
            "waba_name": waba_name,
            "phone_number_id": phone_number_id,
            "phones": phone_number,
            "access_token_json": self.access_token_json
        }
