from django.shortcuts import render
from django.db.models import Q

from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from .models import DirectMessage
from .serializers import (
    DirectMessageSerializer,
    DirectMessageDetailSerializer,
)


class InboxListCreate(generics.ListCreateAPIView):
    """
    GET  -> lista odebranych DMs
    POST -> wyślij wiadomość
    """
    serializer_class = DirectMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return messages for the logged in user.

        Supports filtering by the ``read`` query parameter. ``?read=true`` or
        ``?read=false`` will limit the results accordingly. Any other value is
        ignored and the full set is returned.
        """
        qs = DirectMessage.objects.filter(recipient=self.request.user)
        read_param = self.request.query_params.get("read")
        if read_param is not None:
            lower = read_param.lower()
            if lower in ("true", "1"):
                qs = qs.filter(read=True)
            elif lower in ("false", "0"):
                qs = qs.filter(read=False)
        return qs.order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class OutboxList(generics.ListAPIView):
    """
    Lista wiadomości wysłanych przez użytkownika.
    """
    serializer_class = DirectMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DirectMessage.objects.filter(sender=self.request.user)


class DirectMessageDetail(generics.RetrieveUpdateAPIView):
    """
    Podgląd pojedynczej wiadomości
    PATCH -> oznaczenie przeczytanej (read=True) przez odbiorcę
    """
    serializer_class = DirectMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return DirectMessage.objects.filter(
            Q(sender=user) | Q(recipient=user)
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.recipient == request.user and not instance.read:
            instance.read = True
            instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class DirectMessageViewSet(viewsets.ModelViewSet):
    """ViewSet providing list, create and retrieve actions for messages."""

    serializer_class = DirectMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return DirectMessage.objects.filter(
            Q(sender=user) | Q(recipient=user)
        ).order_by("-created_at")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.recipient == request.user and not instance.read:
            instance.read = True
            instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action in ["retrieve", "partial_update", "update"]:
            return DirectMessageDetailSerializer
        return DirectMessageSerializer

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

