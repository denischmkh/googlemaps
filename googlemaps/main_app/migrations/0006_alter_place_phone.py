# Generated by Django 5.1.7 on 2025-04-02 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_alter_place_num_reviews_alter_place_postcode_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='phone',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='Phone Number'),
        ),
    ]
