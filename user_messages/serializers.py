from rest_framework import serializers
from .models import Message
from django.contrib.auth.models import User

class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.ReadOnlyField(source="sender.username")
    recipient_username = serializers.ReadOnlyField(source="recipient.username")

    # Custom field for recipient validation
    recipient = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        error_messages={
            "does_not_exist": "The specified recipient does not exist.",
            "invalid": "Invalid recipient provided."
        }
    )

    class Meta:
        model = Message
        fields = [
            "id",
            "sender",  # Tylko do odczytu
            "recipient",
            "sender_username",
            "recipient_username",
            "subject",
            "content",
            "created_at",
            "is_read",
        ]
        read_only_fields = ["sender"] 