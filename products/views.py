from django.db.models import Q
from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from drf_api.permissions import IsOwnerOrReadOnly


# Custom pagination class to disable pagination
class NoPagination(PageNumberPagination):
    page_size = None  # Disables pagination by setting no limit


# Product List view (with search and category filters)
class ProductList(generics.ListCreateAPIView):
    """
    List all products or create a new product if logged in.
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ProductSerializer

    def get_queryset(self):
        """
        Filters products by 'search' and 'category' query parameters.

        """
        queryset = Product.objects.all()  # Fetch all products by default
        search = self.request.query_params.get(
            "search", None
        )  # Get search term from query params
        category_id = self.request.query_params.get(
            "category", None
        )  # Get category ID from query params

        if search:  # Filter products if search term exists
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )

        if category_id:  # If a category is specified, filter by category
            queryset = queryset.filter(category__id=category_id)

        return queryset

    def perform_create(self, serializer):
        """
        Automatically assign the current logged-in user as the owner
        of the created product.
        """
        serializer.save(owner=self.request.user)


# Product Detail view (Retrieve, Update, Delete)
class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a product instance if the user owns it.
    """

    permission_classes = [IsOwnerOrReadOnly]  # Owner can modify/delete
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# Category List view (List and create categories)
class CategoryList(generics.ListCreateAPIView):
    """
    List all categories or create a new category if logged in.
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = NoPagination  # Disable pagination for this view


# Category Detail view (Retrieve, Update, Delete)
class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a category instance.
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
