# Generated by Django 5.1.6 on 2025-04-04 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0023_place_country_place_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='open_24_7',
            field=models.CharField(default='No', verbose_name='Open 24/7'),
        ),
    ]
