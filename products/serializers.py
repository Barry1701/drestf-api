from rest_framework import serializers
from .models import Product
from tags.models import Tag


class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    tags = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Tag.objects.all()
    )



    class Meta:
        model = Product
        fields = ['id', 'owner', 'name', 'description', 
                  'image', 'created_at', 'updated_at','tags'
        ]