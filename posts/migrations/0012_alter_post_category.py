# Generated by Django 4.2 on 2024-12-27 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0011_post_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="category",
            field=models.CharField(
                blank=True,
                choices=[
                    ("eczema", "Eczema"),
                    ("allergy", "Allergy"),
                    ("general", "General"),
                ],
                default="general",
                max_length=50,
                null=True,
            ),
        ),
    ]