from django.db.models import Count
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Post
from .serializers import PostSerializer


class PostList(generics.ListCreateAPIView):
    """
    Lists posts or creates a new post if the user is logged in.
    The 'perform_create' method associates the post with the requesting user
    and adds validation logic for 'tags'.
    """

    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.annotate(
        likes_count=Count("likes", distinct=True),
        comments_count=Count("comment", distinct=True),
    ).order_by("-created_at")
    filter_backends = [filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = [
        "owner__followed__owner__profile",
        "likes__owner__profile",
        "owner__profile",
        "category",
    ]
    search_fields = ["owner__username", "title", "category"]
    ordering_fields = ["likes_count", "comments_count", "likes__created_at", "category"]

    def perform_create(self, serializer):
        """
        Validates the 'tags' array from the request data before saving.
        """
        tags = self.request.data.get("tags", [])

        # Ensure 'tags' is an array (e.g., a list of strings)
        if not isinstance(tags, list):
            raise ValidationError({"detail": "'tags' must be an array of strings."})

        # Check maximum length of each tag (30 chars in this example)
        for t in tags:
            if len(t) > 30:
                raise ValidationError({"detail": f"Tag '{t}' is too long (max 30 chars)."})
        
        # If validation passes, associate the post with the current user
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves a post, allows edits or deletion if the user is the owner.
    Includes similar 'tags' validation in 'perform_update'.
    """

    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.annotate(
        likes_count=Count("likes", distinct=True),
        comments_count=Count("comment", distinct=True),
    ).order_by("-created_at")

    def perform_update(self, serializer):
        """
        Validates 'tags' array on update (PUT/PATCH).
        """
        tags = self.request.data.get("tags", [])

        if not isinstance(tags, list):
            raise ValidationError({"detail": "'tags' must be an array of strings."})
        
        for t in tags:
            if len(t) > 30:
                raise ValidationError({"detail": f"Tag '{t}' is too long (max 30 chars)."})
        
        serializer.save()
