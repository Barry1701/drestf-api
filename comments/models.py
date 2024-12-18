from django.db import models
from django.contrib.auth.models import User
from posts.models import Post


class Comment(models.Model):
    """
    Comment model, related to User and Post
    """

    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('question', 'Question'),
        ('tip', 'Tip'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()
    category = models.CharField(
        max_length=50, 
        choices=CATEGORY_CHOICES, 
        default='general',
    )

    class Meta:
        ordering = ["-created_at", "category"]

    def __str__(self):
        return f"{self.owner.username} - {self.get_category_display()}"