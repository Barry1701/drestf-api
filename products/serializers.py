from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

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
            'image', 'created_at', 'updated_at',
        ]
