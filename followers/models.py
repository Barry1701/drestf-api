from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Follower(models.Model):
    owner = models.ForeignKey(
        User, related_name="following", on_delete=models.CASCADE
    )
    followed = models.ForeignKey(
        User, related_name="followed", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "followed"], name="unique_follower"
            )
        ]

    def clean(self):
        """
        Prevent users from following themselves.
        """
        if self.owner == self.followed:
            raise ValidationError("You cannot follow yourself.")

    def save(self, *args, **kwargs):
        """
        Overriding save to include clean method.
        """
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.owner} follows {self.followed}"
