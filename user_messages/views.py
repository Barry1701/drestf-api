from rest_framework import generics, permissions
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Message
from .serializers import MessageSerializer
from rest_framework.exceptions import PermissionDenied



class MessageList(generics.ListCreateAPIView):
    """
    API endpoint to list all messages for the logged-in user or create a new message.

    - Requires authentication.
    - Lists only messages where the logged-in user is the recipient.
    - Allows logged-in users to create new messages.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        """
        Restrict the messages to those received by the logged-in user.
        """
        user = self.request.user
        return Message.objects.filter(recipient=user)

    def perform_create(self, serializer):
        """
        Automatically set the logged-in user as the sender of the new message.
        """
        serializer.save(sender=self.request.user)


class MessageDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint to retrieve, update, or delete a specific message for the logged-in user.

    - Requires authentication.
    - Ensures the logged-in user is the recipient of the requested message.
    """
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = MessageSerializer

    def get_queryset(self):
        """
        Restrict access to messages where the logged-in user is the recipient.
        """
        user = self.request.user
        return Message.objects.filter(recipient=user)
