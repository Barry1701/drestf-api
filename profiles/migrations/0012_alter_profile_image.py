# Generated by Django 5.1.1 on 2024-10-20 17:17

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0011_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=cloudinary.models.CloudinaryField(default='https://res.cloudinary.com/dprwuhawr/image/upload/v1729293609/default_profile_xysrop.jpg', max_length=255, verbose_name='image'),
        ),
    ]
