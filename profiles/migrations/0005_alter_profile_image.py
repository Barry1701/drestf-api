# Generated by Django 5.1.1 on 2024-11-02 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default_profile_uj9rfd', upload_to='images/'),
        ),
    ]