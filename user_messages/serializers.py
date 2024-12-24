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
        read_only_fields = ["sender", "recipient", "subject", "content", "created_at"]

    def update(self, instance, validated_data):
        """
        Limit updates to the 'is_read' field only.
        """
        if "is_read" in validated_data:
            instance.is_read = validated_data["is_read"]
            instance.save()
            return instance
        raise serializers.ValidationError("Only the 'is_read' field can be updated.")