from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

ALLERGY_CHOICES = [
    ('none', 'No Specific Allergy'),
    ('milk', 'Milk Allergy'),
    ('nuts', 'Nut Allergy'),
    ('wheat', 'Wheat Allergy'),
    ('eggs', 'Egg Allergy'),
    ('shellfish', 'Shellfish Allergy'),
    ('dairy', 'Dairy Allergy')
]

class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    image = models.ImageField(
        upload_to="images/",
        default="../profile_ars7c2"
    )

    
    allergy_type = models.CharField(
        max_length=20,
        choices=ALLERGY_CHOICES,
        default='none'
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.owner}'s profile"


def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(owner=instance)


post_save.connect(create_profile, sender=User)
