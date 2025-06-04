from django.shortcuts import render
from django.db.models import Q

from rest_framework import generics, permissions, viewsets
from .models import DirectMessage
from .serializers import DirectMessageSerializer


class InboxListCreate(generics.ListCreateAPIView):
    """
    GET  -> lista odebranych DMs
    POST -> wyślij wiadomość
    """
    serializer_class = DirectMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # tylko wiadomości do zalogowanego usera
        return DirectMessage.objects.filter(recipient=self.request.user)

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


class DirectMessageViewSet(viewsets.ModelViewSet):
    """ViewSet providing list, create and retrieve actions for messages."""

    serializer_class = DirectMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return DirectMessage.objects.filter(
            Q(sender=user) | Q(recipient=user)
        ).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

