from django.urls import path
from .views import ProductList, ProductDetail, CategoryList, CategoryDetail

app_name = 'products'  # Adding app_name for namespace

urlpatterns = [
    path('', ProductList.as_view(), name='product-list'),
    path('<int:pk>/', ProductDetail.as_view(), name='product-detail'),
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetail.as_view(), name='category-detail'),
]
