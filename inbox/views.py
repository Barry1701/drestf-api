from django.shortcuts import render

from rest_framework import generics, permissions
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
            models.Q(sender=user) | models.Q(recipient=user)
        )

