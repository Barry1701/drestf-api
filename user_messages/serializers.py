from rest_framework import serializers
from .models import Message
from django.contrib.auth.models import User

class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.ReadOnlyField(source="sender.username")
    recipient_username = serializers.ReadOnlyField(source="recipient.username")

    # Ensure `recipient` field validation allows only existing users
    recipient = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        error_messages={
            "does_not_exist": "The specified recipient does not exist.",
            "invalid": "Invalid recipient provided.",
        }
    )

    class Meta:
        model = Message
        fields = [
            "id",
            "sender",  # Read-only
            "recipient",  # Recipient provided at creation, cannot be modified
            "sender_username",  # Read-only
            "recipient_username",  # Read-only
            "subject",
            "content",
            "created_at",  # Read-only
            "is_read",
        ]
        read_only_fields = ["sender", "sender_username", "recipient_username", "created_at"]
