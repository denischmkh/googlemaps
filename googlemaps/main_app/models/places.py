import os.path
import sys

from django.db import models
from django.utils import timezone
from django.core.validators import URLValidator, RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator

sys.path.append(os.path.join(os.getcwd(), '..'))

from .countries import City, State
from .categories import Category

from django.utils.text import slugify
from unidecode import unidecode

class Place(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="places", verbose_name="Category")#
    name = models.CharField(max_length=250, verbose_name="Place Name") #
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True, verbose_name="Place Slug")#

    rating = models.FloatField(default=0, null=True, blank=True, verbose_name="Rating",validators=[MinValueValidator(0), MaxValueValidator(5)])#
    num_reviews = models.IntegerField(default=0, null=True, blank=True, verbose_name="Number of Reviews")#
    reviews_list = models.JSONField(null=True, blank=True, verbose_name="Reviews")

    about = models.TextField(blank=True, null=True, verbose_name="About Place")
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, related_name="places", verbose_name="City")#

    full_address = models.CharField(max_length=512, null=True, blank=True, verbose_name="Full Address")#
    address = models.CharField(max_length=250, null=True, blank=True, verbose_name="Street Address")
    located_in = models.CharField(max_length=250, null=True, blank=True, verbose_name="Located In")#
    postcode = models.IntegerField(null=True, blank=True, verbose_name="Postcode")

    lat = models.FloatField(null=True, blank=True, verbose_name="Latitude")#
    lng = models.FloatField(null=True, blank=True, verbose_name="Longitude")#

    place_type = models.CharField(max_length=100, null=True, verbose_name="Type of Place")#
    open_hours = models.CharField(null=True, blank=True, verbose_name="Opening Hours")#
    open_24_7 = models.BooleanField(default=False, verbose_name="Open 24/7")#

    phone = models.CharField(
        max_length=32,
        null=True,
        blank=True,
        verbose_name="Phone Number",
    )#
    email = models.EmailField(null=True, blank=True, verbose_name="Email Address")#

    website = models.URLField(max_length=1000,null=True, blank=True, verbose_name="Website", validators=[URLValidator()])
    clear_website = models.CharField(max_length=250, null=True, verbose_name="Website Domain")#

    facebook = models.URLField(max_length=10000, null=True, blank=True, verbose_name="Facebook")
    instagram = models.URLField(max_length=10000, null=True, blank=True, verbose_name="Instagram")
    linkedin = models.URLField(max_length=10000, null=True, blank=True, verbose_name="LinkedIn")
    youtube = models.URLField(max_length=10000, null=True, blank=True, verbose_name="YouTube")
    twitter = models.URLField(max_length=10000, null=True, blank=True, verbose_name="Twitter")

    link = models.CharField(max_length=10000, null=True, verbose_name="Google Maps Link")#

    status = models.CharField(
        max_length=20,
        choices=[("published", "Published"), ("unpublished", "Unpublished"), ("pending", "Pending")],
        default="unpublished",
        verbose_name="Publication Status",
    )

    created_at = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Created At")

    class Meta:
        verbose_name = "Place"
        verbose_name_plural = "Places"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["city"]),
            models.Index(fields=["category"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            # Транслитерируем кириллицу в латиницу
            slug_base = slugify(unidecode(self.name))  # Преобразуем имя в слаг
            self.slug = slug_base

            # Проверяем уникальность слага и добавляем суффикс, если слаг уже существует
            counter = 1
            while Place.objects.filter(slug=self.slug).exists():
                # Добавляем числовой суффикс, если слаг уже существует
                self.slug = f"{slug_base}-{counter}"
                counter += 1
                
        """Auto-generate `clear_website` from `website`."""
        if self.website:
            self.clear_website = self.website.replace("https://", "").replace("http://", "").split("/")[0]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name