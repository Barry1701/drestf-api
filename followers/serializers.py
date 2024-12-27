from django.db import IntegrityError
from rest_framework import serializers
from .models import Follower


class FollowerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Follower model
    Create method handles the unique constraint on 'owner' and 'followed'
    """

    owner = serializers.ReadOnlyField(source="owner.username")
    followed_name = serializers.ReadOnlyField(source="followed.username")

    class Meta:
        model = Follower
        fields = ["id", "owner", "created_at", "followed", "followed_name"]

    def validate(self, attrs):
        """
        Validate that a user is not trying to follow themselves.
        """
        if self.context["request"].user == attrs["followed"]:
            raise serializers.ValidationError(
                {"detail": "You cannot follow yourself."}
            )
        return attrs

    def create(self, validated_data):
        """
        Handle unique constraint violations gracefully.
        """
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                {"detail": "You are already following this user."}
            )
