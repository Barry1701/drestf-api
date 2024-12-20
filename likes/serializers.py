from django.db import IntegrityError
from rest_framework import serializers
from likes.models import Like


class LikeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Like model
    The create method handles the unique constraint on 'owner' and 'post'
    """

    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Like
        fields = ["id", "created_at", "owner", "post"]

    def validate(self, attrs):
        """
        Ensure that the same user cannot like the same post more than once.
        """
        request = self.context.get("request")
        if request and Like.objects.filter(owner=request.user, post=attrs["post"]).exists():
            raise serializers.ValidationError({"detail": "You have already liked this post."})
        return attrs

    def create(self, validated_data):
        """
        Handle IntegrityError to prevent duplicate likes.
        """
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({"detail": "You have already liked this post."})
