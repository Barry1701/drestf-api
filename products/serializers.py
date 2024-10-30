from rest_framework import serializers
from .models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    # Pole do odczytu, które zwraca nazwę kategorii
    category_name = serializers.ReadOnlyField(source='category.name')
    # Pole do zapisu, które pozwala na wybór kategorii po jej ID
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    def validate_image(self, value):
        if value.size > 2 * 1024 * 1024:  # Ograniczenie do 2 MB
            raise serializers.ValidationError('Image size larger than 2MB!')
        if value.image.height > 4096:  # Maksymalna wysokość 4096px
            raise serializers.ValidationError('Image height larger than 4096px!')
        if value.image.width > 4096:  # Maksymalna szerokość 4096px
            raise serializers.ValidationError('Image width larger than 4096px!')
        return value

    class Meta:
        model = Product
        fields = [
            'id', 'owner', 'name', 'description', 
            'image', 'created_at', 'updated_at', 'category', 'category_name',
        ]
