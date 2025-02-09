from rest_framework import serializers
from .models import Profile
from followers.models import Follower

class ProfileSerializer(serializers.ModelSerializer):
    owner_id = serializers.ReadOnlyField(source="owner.id")
    owner = serializers.ReadOnlyField(source="owner.username")
    is_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()
    posts_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()

    # New field to display a human-readable label from allergy_type choices
    allergy_type_display = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context["request"]
        return request.user == obj.owner

    def get_following_id(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            following = Follower.objects.filter(
                owner=user,
                followed=obj.owner
            ).first()
            return following.id if following else None
        return None

    def get_allergy_type_display(self, obj):
        # Returns the human-readable name from allergy_type choices
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
            "allergy_type",          # <--- new field for actual stored value
            "allergy_type_display",  # <--- shows the label (e.g. "Milk Allergy")
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
