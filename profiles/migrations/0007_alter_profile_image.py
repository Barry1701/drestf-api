# Generated by Django 4.2 on 2024-11-27 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='../profile_ars7c2', upload_to='images/'),
        ),
    ]