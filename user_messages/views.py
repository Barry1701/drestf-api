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
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = MessageSerializer

    def get_queryset(self):
        """
        Restrict access to messages where the logged-in user is the sender or recipient.
        """
        user = self.request.user
        return Message.objects.filter(recipient=user) | Message.objects.filter(sender=user)

    def perform_update(self, serializer):
        """
        Allow only the recipient to update the `is_read` field.
        """
        message = self.get_object()
        if self.request.user != message.recipient:
            raise PermissionDenied("You do not have permission to update this message.")
        serializer.save()