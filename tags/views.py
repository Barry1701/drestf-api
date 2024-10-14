from rest_framework import generics, permissions
from .models import Tag
from .serializers import TagSerializer

class TagList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
