# Generated by Django 4.2 on 2024-11-27 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_remove_post_image_filter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, default='../profile_ars7c2', null=True, upload_to='images/'),
        ),
    ]