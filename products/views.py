from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from drf_api.permissions import IsOwnerOrReadOnly

# Custom pagination class to disable pagination
class NoPagination(PageNumberPagination):
    page_size = None  # Disables pagination by setting no limit

class ProductList(generics.ListCreateAPIView):
    """
    List all products or create a new product if logged in.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        """
        Automatically assign the current logged-in user as the owner
        of the created product.
        """
        serializer.save(owner=self.request.user)

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a product instance if the user owns it.
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryList(generics.ListCreateAPIView):
    """
    List all categories or create a new category if logged in.
    Pagination is disabled for this view.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = NoPagination  # Disable pagination for this view

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a category instance.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
