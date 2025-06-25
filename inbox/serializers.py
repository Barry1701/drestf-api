from rest_framework import serializers
from django.contrib.auth.models import User
from .models import DirectMessage

class DirectMessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.ReadOnlyField(source="sender.username")
    # mapowanie pola recipient do username
    recipient = serializers.SlugRelatedField(
        slug_field="username",
        queryset=User.objects.all(),
    )
    recipient_username = serializers.ReadOnlyField(source="recipient.username")
    content = serializers.CharField(source="body")

    class Meta:
        model = DirectMessage
        fields = [
            "id",
            "sender",
            "sender_username",
            "recipient",
            "recipient_username",
            "subject",
            "content",
            "created_at",
            "read",
        ]
        read_only_fields = ["sender", "created_at", "read"]


class DirectMessageDetailSerializer(DirectMessageSerializer):
    """Serializer used for retrieving and updating a single message."""

    class Meta(DirectMessageSerializer.Meta):
        # mozna tylko odczytywać nadawcę i datę
        read_only_fields = ["sender", "created_at"]
