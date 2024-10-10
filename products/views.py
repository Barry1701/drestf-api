from rest_framework import generics, permissions
from .models import Product
from .serializers import ProductSerializer
from drf_api.permissions import IsOwnerOrReadOnly

class ProductList(generics.ListCreateAPIView):
    """
    List all products or create a new product if logged in.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a product instance if you own it.
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
