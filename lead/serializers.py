from rest_framework import serializers
from .models import Lead, Conversation, Message, Tag


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = "__all__"


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"

class ConversationMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["send_by", "message_type", "content", "file", "created_at"]

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
