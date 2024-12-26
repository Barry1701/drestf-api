from rest_framework import serializers
from .models import Message
from django.contrib.auth.models import User

class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.ReadOnlyField(source="sender.username")
    recipient_username = serializers.ReadOnlyField(source="recipient.username")

    class Meta:
        model = Message
        fields = [
            "id",
            "sender",
            "recipient",
            "sender_username",
            "recipient_username",
            "subject",
            "content",
            "created_at",
            "is_read",
        ]
        read_only_fields = ["sender", "recipient", "sender_username", "recipient_username", "subject", "content", "created_at"]