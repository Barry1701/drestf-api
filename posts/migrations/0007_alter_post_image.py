# Generated by Django 5.1.1 on 2024-11-02 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0006_alter_post_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="image",
            field=models.ImageField(
                blank=True,
                default="../default_post_ehnhuw",
                null=True,
                upload_to="images/",
            ),
        ),
    ]
