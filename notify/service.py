from rest_framework import status, exceptions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from .models import ActivityLog, WebhookLog
from integration.models import WhatsAppAccount
from lead.models import Lead, Conversation, Message
from core.choice_select import CONVERSATION_STATUS, MESSAGE_DIRECTION, MESSAGE_TYPE, MESSAGE_STATUS, SEND_BY
from datetime import datetime, timezone
import random
import requests
from django.utils import timezone
from lead.serializers import ConversationMessageSerializer


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
    def __init__(self, payload: dict, webhook_log: object = None):
        self.payload = payload
        self.value = payload["entry"][0]["changes"][0]["value"]

        self.phone_number_id = self.get_phone_number_id()
        self.waba = WhatsAppAccount.objects.filter(phone_number_id=self.phone_number_id, waba_id=self.get_waba_id()).first()

        self.business = self.waba.business if self.waba else None
        
        self.webhook_log = webhook_log
        print("received webhook response from meta!")
    
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

    def create_message(self, lead, conversation):
        message_type = self.message["type"].upper()
        timestamp = datetime.fromtimestamp(int(self.message["timestamp"]))
        text = self.message["text"]["body"]
        mssage_system_id = self.message["id"]

        message_type =  message_type if message_type in MESSAGE_STATUS.choices else MESSAGE_TYPE.TEXT

        msge = Message.objects.create(
            business=self.business,
            whatsapp_account=self.waba,
            lead=lead,
            conversation=conversation,
            direction=MESSAGE_DIRECTION.INCOMING,
            message_type=message_type,
            content=text,
            status=MESSAGE_STATUS.RECEIVED,
            timestamp=timestamp,
            system_id=mssage_system_id,
            send_by=SEND_BY.CLIENT
        )
        return msge
    
    def get_whole_conversation(self, conversation):
        messages = conversation.messages.all()
        business = conversation.business
        business_information = business.business_information_for_ai

        conversation_history = messages
        # for msg in reversed(messages):
        #     role = "Customer" if msg.direction == "incoming" else "Assistant"
        #     conversation_history += f"{role}: {msg.text}\n"

        prompt = f"""
        You are a helpful customer support assistant for this business.

        Business Information:
        Name: {business.name}
        Description: {business.description}
        Services: {business_information.service}
        Industry: {business_information.industry}
        Business Details: {business_information.business_details}
        Product Details: {business_information.product_details}
        Service Details: {business_information.service_details}
        Location: {business.location}

        # - product inquiry
        # - support request
        # - pricing
        # - greeting

        Instructions:
        - Reply like a friendly human support agent
        - Keep answers short and helpful
        - If the user asks about services, explain clearly
        - If you don't know the answer, ask the user for more details
        - Always be polite

        Conversation History:
        {conversation_history}

        User Message:
        {self.message["text"]["body"]}

        Write the best reply for the customer.
        """
        print("prompt: ", prompt)
        serializer = ConversationMessageSerializer(messages, many=True)
        print("conversation data: ", serializer.data)
    
    def send_ai(self, received_message):
        conversation_message = self.get_whole_conversation(received_message.conversation)
        next_message_id = Message.objects.count() + 1
        send_message_data = {
            "business": received_message.business,
            "whatsapp_account": received_message.whatsapp_account,
            "lead": received_message.lead,
            "conversation": received_message.conversation,
            "direction": MESSAGE_DIRECTION.OUTGOING,
            "content": f"Reply Messgage content ({next_message_id})",
            "status": MESSAGE_STATUS.SENT
        }
        send_message = Message.objects.create(
            **send_message_data
        )
        return send_message

    def send_message_to_whatsapp(self, send_message):
        # from .tasks import send_whatsapp_message_tasks
        # send_whatsapp_message_tasks.delay(send_message.id)
        lead = send_message.lead
        whatsapp_account = send_message.whatsapp_account
        access_token_dict = whatsapp_account.access_token
        content = send_message.content

        url = f"https://graph.facebook.com/v18.0/{whatsapp_account.phone_number_id}/messages"
        headers = {
            "Authorization": f"Bearer {access_token_dict.get('access_token')}",
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

        if "messages" in data:
            meta_id = data["messages"][0]["id"]
            send_message.system_id = meta_id
            send_message.save()

        return data

    def handle_message(self):
        try:
            if self.business and self.waba:
                with transaction.atomic():
                    self.contact = self.value["contacts"][0]
                    self.message = self.value["messages"][0]

                    lead = self.get_lead()
                    conversation = self.get_conversation(lead)
                    message = self.create_message(lead, conversation)

                    lead.last_message_at = message.created_at
                    conversation.last_message_at = message.created_at
                    lead.save()
                    conversation.save()

                    send_message = self.send_ai(message)
                    self.send_message_to_whatsapp(send_message)

                    self.webhook_log.processed = True
                    self.webhook_log.business = self.business
                    self.webhook_log.save()
                    print("message processed successfully")
        except Exception as e:
            print("message handling error:", e)

    def handle_status(self):
        try:
            status_data = self.value["statuses"][0]
            message_id = status_data["id"]
            status = status_data["status"]

            status_map = {
                "sent": MESSAGE_STATUS.SENT,
                "delivered": MESSAGE_STATUS.DELIVERED,
                "read": MESSAGE_STATUS.READ,
                "failed": MESSAGE_STATUS.FAILED
            }

            Message.objects.filter(system_id=message_id).update(
                status=status_map.get(status, MESSAGE_STATUS.SENT)
            )
            self.webhook_log.processed = True
            self.webhook_log.save()

            print("status updated:", status_map.get(status, MESSAGE_STATUS.SENT))
        except Exception as e:
            print("status handling error:", e)


    

