from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import DirectMessage

@receiver(post_save, sender=DirectMessage)
def notify_new_message(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"notifications_{instance.recipient.username}",
            {
                "type": "notify",
                "data": {
                    "message": f"New message from {instance.sender.username}",
                    "id": instance.id,
                }
            }
        )

