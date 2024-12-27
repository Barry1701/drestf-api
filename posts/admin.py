from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner', 'category', 'created_at')  # Kolumny w widoku listy
    list_filter = ('category', 'created_at')  # Filtry boczne
    search_fields = ('title', 'content', 'owner__username')  # Pole wyszukiwania
    ordering = ('-created_at',)  # Domyślne sortowanie
