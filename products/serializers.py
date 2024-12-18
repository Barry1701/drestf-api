from rest_framework import serializers
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]


class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    # Read-only field that returns the category name
    category_name = serializers.ReadOnlyField(source="category.name")
    # Writeable field that allows selecting the category by its ID
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    def validate_image(self, value):
        # Limit the image size to 2 MB
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError("Image size larger than 2MB!")
        # Set maximum allowed image height to 4096px
        if value.image.height > 4096:
            raise serializers.ValidationError("Image height larger than 4096px!")
        # Set maximum allowed image width to 4096px
        if value.image.width > 4096:
            raise serializers.ValidationError("Image width larger than 4096px!")
        return value

    class Meta:
        model = Product
        fields = [
            "id",
            "owner",
            "name",
            "description",
            "image",
            "created_at",
            "updated_at",
            "category",
            "category_name",
        ]
