# Generated by Django 5.1.6 on 2025-04-04 10:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0037_alter_place_facebook_alter_place_instagram_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='website',
            field=models.URLField(blank=True, max_length=1000, null=True, validators=[django.core.validators.URLValidator()], verbose_name='Website'),
        ),
    ]
