from django.db import models
from django.contrib.auth.models import User
from tags.models import Tag
from cloudinary.models import CloudinaryField



class Post(models.Model):
    """
    Post model, related to 'owner', i.e. a User instance.
    Default image set so that we can always reference image.url.
    """
    image_filter_choices = [
        ('eczema_relief', 'Eczema Relief'), 
        ('dry_skin', 'Dry Skin'),
        ('flare_control', 'Flare Control'),
        ('allergy_block', 'Allergy Block'),
        ('soothing_care', 'Soothing Care'),
        ('hydration_boost', 'Hydration Boost'),
        ('anti_itch', 'Anti-Itch'),
        ('rash_reducer', 'Rash Reducer'),
        ('calming_effect', 'Calming Effect'),
        ('moisture_lock', 'Moisture Lock'),
        ('sensitive_skin', 'Sensitive Skin'),
        ('allergy_defense', 'Allergy Defense'),
        ('relief_plus', 'Relief Plus'),
        ('barrier_protect', 'Barrier Protect'),
        ('soothe_and_heal', 'Soothe & Heal'),
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    image = CloudinaryField( 'image', default='https://res.cloudinary.com/dprwuhawr/image/upload/v1728378396/default_post_aczthl.jpg', blank=True
    )
    image_filter = models.CharField(
        max_length=32, choices=image_filter_choices, default='normal'
    )
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.title}'