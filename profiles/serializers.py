from rest_framework import serializers
from .models import Profile
from followers.models import Follower

class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the Profile model.
    Includes fields for counting posts/followers/following,
    and a human-readable display for allergy_type.
    """

    owner_id = serializers.ReadOnlyField(source="owner.id")
    owner = serializers.ReadOnlyField(source="owner.username")
    is_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()
    posts_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()

    # Converts the choice field 'allergy_type' into a human-readable label
    allergy_type_display = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        """
        Determines if the requesting user is the owner of the profile.
        """
        request = self.context["request"]
        return request.user == obj.owner

    def get_following_id(self, obj):
        """
        Returns the id of the 'Follower' relationship if the requesting user
        is following this profile's owner. Otherwise, returns None.
        """
        user = self.context["request"].user
        if user.is_authenticated:
            following = Follower.objects.filter(
                owner=user,
                followed=obj.owner
            ).first()
            return following.id if following else None
        return None

    def get_allergy_type_display(self, obj):
        """
        Provides a human-readable display string for the 'allergy_type' field.
        For example, 'milk' -> 'Milk Allergy'.
        """
        return obj.get_allergy_type_display()

    class Meta:
        model = Profile
        fields = [
            "id",
            "owner",
            "created_at",
            "updated_at",
            "name",
            "content",
            "image",
            "allergy_type",
            "allergy_type_display",
            "is_owner",
            "following_id",
            "posts_count",
            "followers_count",
            "following_count",
            "owner_id",
        ]
        read_only_fields = [
            "owner",
            "created_at",
            "updated_at",
            "owner_id",
            "posts_count",
            "followers_count",
            "following_count",
        ]
