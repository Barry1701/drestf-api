from rest_framework import serializers
from posts.models import Post, Tag
from likes.models import Like

class TagSlugRelatedField(serializers.SlugRelatedField):
    """
    A custom SlugRelatedField that either uses an existing Tag by name,
    or creates a new Tag if one does not exist.
    """

    def to_internal_value(self, data):
        queryset = self.get_queryset()
        slug_field = self.slug_field

        # Attempt to find an existing Tag by 'name' = data
        try:
            obj = queryset.get(**{slug_field: data})
        except Tag.DoesNotExist:
            # If it does not exist, create it
            obj = Tag.objects.create(name=data)
        return obj


class PostSerializer(serializers.ModelSerializer):
    """
    Main serializer for the Post model, including tag logic via TagSlugRelatedField.
    """

    owner = serializers.ReadOnlyField(source="owner.username")
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source="owner.profile.id")
    profile_image = serializers.ReadOnlyField(source="owner.profile.image.url")
    like_id = serializers.SerializerMethodField()
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()

    # Use the custom field for tags
    tags = TagSlugRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        slug_field='name',
        required=False
    )

    def validate_image(self, value):
        # Check image size; raise error if it exceeds 2MB
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError("Image size larger than 2MB!")
        # Validate image dimensions, ensuring they are within the 4096px limit
        if value.image.height > 4096:
            raise serializers.ValidationError("Image height larger than 4096px!")
        if value.image.width > 4096:
            raise serializers.ValidationError("Image width larger than 4096px!")
        return value

    def get_is_owner(self, obj):
        request = self.context["request"]
        return request.user == obj.owner

    def get_like_id(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            like = Like.objects.filter(owner=user, post=obj).first()
            return like.id if like else None
        return None

    class Meta:
        model = Post
        fields = [
            "id",
            "owner",
            "is_owner",
            "profile_id",
            "profile_image",
            "created_at",
            "updated_at",
            "title",
            "content",
            "image",
            "category",
            "like_id",
            "likes_count",
            "comments_count",
            "tags",
        ]
