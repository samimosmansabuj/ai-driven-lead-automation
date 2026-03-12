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
        print("token_data: ", token_data)
        access_token = token_data.get("access_token")
        if not access_token:
            raise Exception("Token exchange failed")
        return access_token
    
    def get_access_token(self):
        if self.token_type == "access_code":
            access_token = self.exchange_code_for_token()
            return access_token
        elif self.token_type == "access_token":
            return self.token

    def get_user_businesses(self):
        url = "https://graph.facebook.com/v23.0/me?fields=id,name,accounts,businesses&access_token=" + self.get_access_token()
        resp = requests.get(url)
        return resp.json().get("businesses", {}).get("data", [])

    def get_whatsapp_accounts_for_business(self, business_id):
        url = f"https://graph.facebook.com/v18.0/{business_id}"
        params = {
            "fields": "owned_whatsapp_business_accounts",
            "access_token": self.get_access_token()
        }
        resp = requests.get(url, params=params)
        return resp.json()

    # def get_own_whatsapp_accounts_for_business(self):
    #     url = "https://graph.facebook.com/v23.0/me?fields=businesses{owned_whatsapp_business_accounts}&access_token=" + self.get_access_token()
    #     resp = requests.get(url)
    #     return resp.json().get("businesses", {}).get("data", [])
    
    def get_phone_numbers(self, waba_id):
        url = f"https://graph.facebook.com/v18.0/{waba_id}/phone_numbers"
        params = {"access_token": self.get_access_token()}
        resp = requests.get(url, params=params)
        return resp.json().get("data", [])

    def connected(self):
        businesses = self.get_user_businesses()
        if not businesses:
            raise Exception("No business information found")
        print("businesses: ", businesses)
        business = businesses[0]
        business_id = business["id"]

        waba_data = self.get_whatsapp_accounts_for_business(business_id)
        if not waba_data:
            raise Exception("No Whatsapp business accont found")
        print("waba_data: ", waba_data)

        # get_own_whatsapp_accounts_for_business = self.get_own_whatsapp_accounts_for_business()

        waba_id = waba_data.get("owned_whatsapp_business_accounts", {}).get("data", [])[0].get("id")
        waba_name = waba_data.get("owned_whatsapp_business_accounts", {}).get("data", [])[0].get("name")

        phones = self.get_phone_numbers(waba_id)
        if not phones:
            raise Exception("No phone number found")
        print("phones: ", phones)
        phone_number = phones[0].get("display_phone_number")
        phone_number_id = phones[0].get("id")
        to_number = "+8801533125837"
        return {
            "status": "connected",
            "business_id": business_id,
            "waba_id": waba_id,
            "waba_name": waba_name,
            "phones": phone_number
        }
