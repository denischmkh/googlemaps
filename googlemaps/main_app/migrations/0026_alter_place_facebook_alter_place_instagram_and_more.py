# Generated by Django 5.1.6 on 2025-04-04 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0025_alter_place_lat_alter_place_lng_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='facebook',
            field=models.TextField(blank=True, null=True, verbose_name='Facebook'),
        ),
        migrations.AlterField(
            model_name='place',
            name='instagram',
            field=models.TextField(blank=True, null=True, verbose_name='Instagram'),
        ),
        migrations.AlterField(
            model_name='place',
            name='link',
            field=models.TextField(null=True, unique=True, verbose_name='Google Maps Link'),
        ),
        migrations.AlterField(
            model_name='place',
            name='linkedin',
            field=models.TextField(blank=True, null=True, verbose_name='LinkedIn'),
        ),
        migrations.AlterField(
            model_name='place',
            name='twitter',
            field=models.TextField(blank=True, null=True, verbose_name='Twitter'),
        ),
        migrations.AlterField(
            model_name='place',
            name='youtube',
            field=models.TextField(blank=True, null=True, verbose_name='YouTube'),
        ),
    ]
