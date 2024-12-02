from django.db.models import Q
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
    serializer_class = ProductSerializer

    def get_queryset(self):
        """
        Optionally filters products by 'search' and 'category' parameters in the URL.
        """
        queryset = Product.objects.all()
        search = self.request.query_params.get('search', None)
        category_id = self.request.query_params.get('category', None)

        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(description__icontains=search))

        if category_id:
            queryset = queryset.filter(category__id=category_id)

        return queryset

    def perform_create(self, serializer):
        """
        Automatically assign the current logged-in user as the owner
        of the created product.
        """
        serializer.save(owner=self.request.user)
