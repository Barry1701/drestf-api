# Generated by Django 5.1.1 on 2024-10-17 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='../default_profile_b0dubq', upload_to='images/'),
        ),
    ]