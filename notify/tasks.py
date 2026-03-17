# from celery import shared_task
# from .models import WebhookLog
# from .service import WebhookLogModule
# import requests
# from celery import shared_task
# from lead.models import Message
# from django.utils import timezone

# @shared_task
# def process_webhook(log_id):
#     webhook_log = WebhookLog.objects.get(id=log_id)
#     payload = webhook_log.payload
#     module = WebhookLogModule(payload, webhook_log)
    
#     value = payload["entry"][0]["changes"][0]["value"]
#     if "messages" in value:
#         module.handle_message()
#     elif "statuses" in value:
#         module.handle_status()


# @shared_task(bind=True, max_retries=3)
# def send_whatsapp_message_tasks(self, message_id):
#     message = Message.objects.get(id=message_id)
#     try:
#         url = f"https://graph.facebook.com/v18.0/{message.whatsapp_account.phone_number_id}/messages"
#         headers = {
#             "Authorization": f"Bearer {message.whatsapp_account.access_token['access_token']}",
#             "Content-Type": "application/json"
#         }
#         payload = {
#             "messaging_product": "whatsapp",
#             "to": message.lead.phone_number,
#             "type": "text",
#             "text": {"body": message.content}
#         }
#         response = requests.post(url, json=payload, headers=headers)
#         data = response.json()
        
#         if "messages" in data:
#             message.system_id = data["messages"][0]["id"]
#             message.save()
#     except Exception as exc:
#         raise self.retry(exc=exc, countdown=5)
