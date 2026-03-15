from rest_framework import status, exceptions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from .models import ActivityLog, WebhookLog
from integration.models import WhatsAppAccount
from lead.models import Lead, Conversation, Message
from core.choice_select import CONVERSATION_STATUS, MESSAGE_DIRECTION, MESSAGE_TYPE, MESSAGE_STATUS
from datetime import datetime, timezone
import random
import requests

class LogActivityModule:
    def get_confirm_data(self, field, field_name):
        if not field:
            raise Exception(f"{field_name} is missing.")
        return field
    
    def __init__(self, data: dict):
        user = data.get("user")
        if hasattr(user, "user"):
            user = user.user
        
        self.user = self.get_confirm_data(user, "User")
        self.business = data.get("business")
        self.action = self.get_confirm_data(data.get("action"), "Action")
        self.entity = data.get("entity")
        self.request = self.get_confirm_data(data.get("request"), "Request")
        self.metadata = data.get("metadata", {})
        self.need_notify = data.get("for_notify", False)
    
    def get_entity_type(self):
        if self.entity is None:
            return None
        elif not hasattr(self.entity, "_meta"):
            raise Exception("Entity must be a Django model instance.")
        else:
            return ContentType.objects.get_for_model(self.entity)

    def get_ip(self, request):
        xff = request.META.get("HTTP_X_FORWARDED_FOR")
        if xff:
            return xff.split(",")[0]
        return request.META.get("REMOTE_ADDR")

    def get_data(self):
        dict_data = {
            "user": self.user,
            "action": self.action,
            "metadata": self.metadata,
            "ip_address": self.get_ip(self.request),
            "need_notify": self.need_notify
        }
        if self.business:
            dict_data["business"] = self.business
        if self.entity:
            dict_data["entity_type"] = self.get_entity_type()
            dict_data["entity_id"] = self.entity.id
        return dict_data

    def create(self):
        try:
            with transaction.atomic():
                log = ActivityLog.objects.create(
                    **self.get_data()
                )
                return log
        except Exception as e:
            print("error: ", e)
            raise Exception("Someting wrong for create log!")



class WebhookLogModule:
    def __init__(self, payload: dict):
        self.payload = payload
        self.phone_number_id = self.get_phone_number_id()

        # print("self.payload: ", self.payload)
        # print("phone number id: ", self.phone_number_id)
        # print("wpba id: ", self.get_waba_id())

        self.waba = WhatsAppAccount.objects.filter(phone_number_id=self.phone_number_id, waba_id=self.get_waba_id()).first()
        # print("self.waba: ", self.waba)

        self.business = self.waba.business if self.waba else None
        # print("self.business: ", self.business)

        self.create_log()

        self.contact = payload["entry"][0]["changes"][0]["value"]["contacts"][0]
        self.message = payload["entry"][0]["changes"][0]["value"]["messages"][0]
    
    def get_lead(self):
        name = self.contact["profile"]["name"]
        lead_number = self.contact["wa_id"]
        lead, created = Lead.objects.get_or_create(
            business=self.business,
            whatsapp_account=self.waba,
            phone_number=lead_number,
            defaults={
                "name": name
            }
        )
        return lead
    
    def get_conversation(self, lead):
        conversation, created = Conversation.objects.get_or_create(
            status=CONVERSATION_STATUS.OPEN,
            business=self.business,
            whatsapp_account=self.waba,
            lead=lead,
        )
        return conversation

    def get_phone_number_id(self):
        return self.payload["entry"][0]["changes"][0]["value"]["metadata"]["phone_number_id"]
    
    def get_waba_id(self):
        return self.payload["entry"][0]["id"]

    def create_log(self):
        webhook_log = WebhookLog.objects.create(
            business=self.business,
            payload=self.payload,
            event_type="whatsapp_message",
            processed=False
        )
        self.webhook_log = webhook_log
        return webhook_log

    def create_message(self, lead, conversation, ):
        message_type = self.message["type"].upper()
        message_id = self.message["id"]
        timestamp = datetime.fromtimestamp(int(self.message["timestamp"]))
        text = self.message["text"]["body"]
        message_type =  message_type if message_type in MESSAGE_STATUS.choices else MESSAGE_TYPE.TEXT
        msge = Message.objects.create(
            business=self.business,
            whatsapp_account=self.waba,
            lead=lead,
            conversation=conversation,
            direction=MESSAGE_DIRECTION.INCOMING,
            message_type=message_type,
            content=text,
            meta_message_id=message_id,
            status=MESSAGE_STATUS.RECEIVED,
            timestamp=timestamp
        )
        return msge
    
    def send_ai(self, received_message):
        # send message and business information to AI 
        next_message_id = received_message.id + 1
        send_message_data = {
            "business": received_message.business,
            "whatsapp_account": received_message.whatsapp_account,
            "lead": received_message.lead,
            "conversation": received_message.conversation,
            "direction": MESSAGE_DIRECTION.OUTGOING,
            "content": f"Reply Messgage content ({next_message_id})",
            "status": MESSAGE_STATUS.SENT,
        }
        send_message = Message.objects.create(
            # **send_message_data
            business = received_message.business,
            whatsapp_account = received_message.whatsapp_account,
            lead = received_message.lead,
            conversation = received_message.conversation,
            direction = MESSAGE_DIRECTION.OUTGOING,
            content = f"Reply Messgage content ({next_message_id})",
            status = MESSAGE_STATUS.SENT,
        )
        return send_message

    def send_message_to_whatsapp(self, send_message):
        lead = send_message.lead
        whatsapp_account = send_message.whatsapp_account
        access_token_dict = whatsapp_account.access_token
        content = send_message.content

        url = f"https://graph.facebook.com/v18.0/{whatsapp_account.phone_number_id}/messages"
        headers = {
            "Authorization": f"Bearer {access_token_dict.get("access_token")}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": lead.phone_number,
            "type": "text",
            "text": {
                "body": content
            }
        }

        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        print("data: ", data)
        return data

    def make_response(self):
        try:
            if self.business and self.waba:
                self.webhook_log.processed = True
                self.webhook_log.save()
                with transaction.atomic():
                    lead = self.get_lead()
                    conversation = self.get_conversation(lead)
                    message = self.create_message(lead, conversation)

                    lead.last_message_at = message.created_at
                    conversation.last_message_at = message.created_at
                    lead.save()
                    conversation.save()

                    # send message and business information to AI 
                    send_message = self.send_ai(self, message)
                    print("send_message: ", send_message)
                    self.send_message_to_whatsapp(send_message)

                    # send message to client 
                    return True
        except Exception as e:
            return False

        

    

