from rest_framework import serializers
from django.contrib.auth.models import User
from .models import DirectMessage


class DirectMessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.ReadOnlyField(source="sender.username")
    receiver = serializers.SlugRelatedField(
        source="recipient",
        slug_field="username",
        queryset=User.objects.all(),
    )
    receiver_username = serializers.ReadOnlyField(source="recipient.username")
    content = serializers.CharField(source="body")

    class Meta:
        model = DirectMessage
        fields = [
            "id",
            "sender",
            "sender_username",
            "receiver",
            "receiver_username",
            "subject",
            "content",
            "created_at",
            "read",
        ]
        read_only_fields = ["sender", "created_at", "read"]
