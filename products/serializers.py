from rest_framework import serializers
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.
    """

    class Meta:
        model = Category
        fields = ["id", "name", "description"]


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.
    Includes additional read-only and validation logic.
    """

    owner = serializers.ReadOnlyField(source="owner.username")
    category_name = serializers.ReadOnlyField(source="category.name")
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )

    def validate_image(self, value):
        """
        Validate the uploaded image's size, height, and width.
        """
        max_size = 2 * 1024 * 1024  # 2MB
        max_dimension = 4096  # 4096px

        if value.size > max_size:
            raise serializers.ValidationError(
                "Image size larger than 2MB!"
            )

        if value.image.height > max_dimension:
            raise serializers.ValidationError(
                "Image height larger than 4096px!"
            )

        if value.image.width > max_dimension:
            raise serializers.ValidationError(
                "Image width larger than 4096px!"
            )

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
