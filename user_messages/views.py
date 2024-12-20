from rest_framework import generics, permissions
from .models import Message
from .serializers import MessageSerializer

class MessageList(generics.ListCreateAPIView):
    """
    List all messages for the logged-in user or create a new message.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(recipient=user)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class MessageDetail(generics.RetrieveAPIView):
    """
    Retrieve a specific message for the logged-in user.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(recipient=user)
