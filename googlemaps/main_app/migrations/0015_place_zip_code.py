# Generated by Django 5.1.6 on 2025-04-04 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0014_place_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='zip_code',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
