import os
from openai import OpenAI
from dotenv import load_dotenv
from core.choice_select import SEND_BY

class AIModule:
    def __init__(self, received_message):
        self.received_message = received_message
        self.conversation = received_message.conversation
        self.business = self.conversation.business
        self.business_information = self.business.business_information_for_ai
    
    def get_business_information(self):
        prompt = f"""
Business Information:
Name: {self.business.name}
Description: {self.business.description}
Industry: {self.business_information.industry}
Services: {self.business_information.service}
Business Details: {self.business_information.business_details}
Product Details: {self.business_information.product_details}
Service Details: {self.business_information.service_details}
Location: {self.business.location}
Website: {self.business_information.website}
"""
        return prompt
    
    def get_conversation(self):
        messages = self.conversation.messages.all()[:6]
        conversation_history = []
        for msg in reversed(messages):
            role = "user" if msg.send_by == SEND_BY.CLIENT else "assistant"
            conversation_history.append({"role": role, "content": msg.content})
        return conversation_history

    def get_system_prompt(self):
        prompt = f"""
        You are a helpful customer support assistant for this business.
        
        {self.get_business_information()}

        Instructions & Rules:
        1. Always respond in Bangla.
        2. Be polite and Reply like a friendly human customer support.
        3. Keep answers short and helpful
        4. If the user asks about services, explain clearly
        5. If the user asks about a product, explain briefly and encourage order.
        6. If the user wants to order, collect:
            - Name
            - Address
            - Phone
        7. If you do not know the answer, politely say our support team will assist.
        8. Avoid robotic language

        Write the best reply for the customer.
        """
        return prompt
    
    def generate_reply_with_ai(self):
        messages = [{"role": "system", "content": self.get_system_prompt()}]
        messages.extend(self.get_conversation())
        messages.append({"role": "user", "content": self.received_message.content})
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            # model="gpt-4o-mini",
            # model="gpt-4", # Or "gpt-3.5-turbo" for lower cost/latency
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        print("=======================================")
        print("response: ", response)
        print("--------------------------------------")
        reply = response.choices[0].message.content
        print("reply: ", reply)
        print("=======================================")
        return reply

