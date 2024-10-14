from django.db import models



class Tag(models.Model):
    """
    Model representing a tag that can be used to categorize posts and products.
    """
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# Update the Post model to include tags
def update_post_model():
    Post.add_to_class('tags', models.ManyToManyField(Tag, related_name='posts', blank=True))
