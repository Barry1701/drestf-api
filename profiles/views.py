from django.db.models import Count
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer

class ProfileList(generics.ListAPIView):
    """
    List all profiles.
    No create view as profile creation is handled by django signals.
    """

    queryset = Profile.objects.annotate(
        posts_count=Count("owner__post", distinct=True),
        followers_count=Count("owner__followed", distinct=True),
        following_count=Count("owner__following", distinct=True),
    ).order_by("-created_at")
    serializer_class = ProfileSerializer

    # Filter and ordering configuration
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
        # text-based search, you could add:
        filters.SearchFilter,
    ]

    # Add "allergy_type" to filterset_fields so you can do: /profiles/?allergy_type=nuts
    filterset_fields = [
        "owner__following__followed__profile",
        "owner__followed__owner__profile",
        "allergy_type",
    ]

    # Fields that can be used in ordering queries: /profiles/?ordering=some_field
    ordering_fields = [
        "posts_count",
        "followers_count",
        "following_count",
        "owner__following__created_at",
        "owner__followed__created_at",
    ]


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update a profile if you're the owner.
    """

    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = ProfileSerializer

    queryset = Profile.objects.annotate(
        posts_count=Count("owner__post", distinct=True),
        followers_count=Count("owner__followed", distinct=True),
        following_count=Count("owner__following", distinct=True),
    ).order_by("-created_at")
