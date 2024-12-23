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

    def validate_subject(self, value):
        """
        Ensure the subject is not empty or only whitespace.
        """
        if not value.strip():
            raise serializers.ValidationError("Subject cannot be blank.")
        return value

    def validate_content(self, value):
        """
        Ensure the content is not empty or only whitespace.
        """
        if not value.strip():
            raise serializers.ValidationError("Content cannot be blank.")
        return value

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
