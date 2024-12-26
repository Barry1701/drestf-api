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
        Prevent users from sending messages to themselves.
        """
        recipient = serializer.validated_data.get("recipient")
        if recipient == self.request.user:
            raise PermissionDenied("You cannot send a message to yourself.")
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
        Restrict access to messages where the logged-in user is the recipient or sender.
        """
        user = self.request.user
        return Message.objects.filter(recipient=user) | Message.objects.filter(sender=user)

    def perform_update(self, serializer):
        """
        Allow updating only the `is_read` field.
        Ensure that only recipients can mark messages as read.
        """
        instance = self.get_object()
        if self.request.user != instance.recipient:
            raise PermissionDenied("Only the recipient can mark a message as read.")
        serializer.save()
