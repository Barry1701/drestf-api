# Generated by Django 5.1.1 on 2024-10-08 14:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, default='../default_post_rgq6aq', upload_to='images/')),
                ('image_filter', models.CharField(choices=[('eczema_relief', 'Eczema Relief'), ('dry_skin', 'Dry Skin'), ('flare_control', 'Flare Control'), ('allergy_block', 'Allergy Block'), ('soothing_care', 'Soothing Care'), ('hydration_boost', 'Hydration Boost'), ('anti_itch', 'Anti-Itch'), ('rash_reducer', 'Rash Reducer'), ('calming_effect', 'Calming Effect'), ('moisture_lock', 'Moisture Lock'), ('sensitive_skin', 'Sensitive Skin'), ('allergy_defense', 'Allergy Defense'), ('relief_plus', 'Relief Plus'), ('barrier_protect', 'Barrier Protect'), ('soothe_and_heal', 'Soothe & Heal')], default='normal', max_length=32)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]