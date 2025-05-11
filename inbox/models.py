from django.db import models
from django.contrib.auth.models import User


class DirectMessage(models.Model):
    """
    Private message between two users.
    """
    sender      = models.ForeignKey(User, related_name="sent_messages",
                                    on_delete=models.CASCADE)
    recipient   = models.ForeignKey(User, related_name="received_messages",
                                    on_delete=models.CASCADE)
    subject     = models.CharField(max_length=255, blank=True)
    body        = models.TextField()
    created_at  = models.DateTimeField(auto_now_add=True)
    read        = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"DM from {self.sender} to {self.recipient} ({self.subject})"

