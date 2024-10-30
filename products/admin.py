from django.contrib import admin
from .models import Product, Category  # Dodaj Category, jeśli istnieje

# Zarejestruj oba modele w panelu admina
admin.site.register(Product)
admin.site.register(Category)