from django.contrib import admin
from .models import Product, Category  # Add Category if it exists

# Register both models in the admin panel
admin.site.register(Product)
admin.site.register(Category)
