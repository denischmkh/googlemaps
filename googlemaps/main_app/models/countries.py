from django.db import models

from django.utils.text import slugify
from unidecode import unidecode

class Country(models.Model):
    full_name = models.CharField(max_length=128, unique=True, verbose_name="Full Name")
    iso_code_2 = models.CharField(max_length=2, unique=True, null=True, blank=True, verbose_name="ISO Code (2 letters)")
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True, verbose_name="Country Slug")

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        ordering = ["full_name"]

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if not self.slug:
            # Транслитерируем кириллицу в латиницу
            slug_base = slugify(unidecode(self.full_name))  # Преобразуем имя в слаг
            self.slug = slug_base

            # Проверяем уникальность слага и добавляем суффикс, если слаг уже существует
            counter = 1
            while Country.objects.filter(slug=self.slug).exists():
                # Добавляем числовой суффикс, если слаг уже существует
                self.slug = f"{slug_base}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

class State(models.Model):
    full_name = models.CharField(max_length=128, verbose_name="State Name")
    iso_code_2 = models.CharField(max_length=2, null=True, verbose_name="ISO Code (2 letters)")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="states", verbose_name="Country")
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True, verbose_name="State Slug")

    class Meta:
        verbose_name = "State"
        verbose_name_plural = "States"
        ordering = ["full_name"]
        unique_together = ("country", "full_name")

    def __str__(self):
        return self.full_name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # Транслитерируем кириллицу в латиницу
            slug_base = slugify(unidecode(self.full_name))  # Преобразуем имя в слаг
            self.slug = slug_base

            # Проверяем уникальность слага и добавляем суффикс, если слаг уже существует
            counter = 1
            while State.objects.filter(slug=self.slug).exists():
                # Добавляем числовой суффикс, если слаг уже существует
                self.slug = f"{slug_base}-{counter}"
                counter += 1
        super().save(*args, **kwargs)


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="cities", verbose_name="Country")
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="cities", verbose_name="State", null=True, blank=True)
    full_name = models.CharField(max_length=128, verbose_name="Full Name")
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True, verbose_name="City Slug")

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"
        ordering = ["full_name"]
        unique_together = ("state", "full_name")

    def __str__(self):
        return self.full_name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # Транслитерируем кириллицу в латиницу
            slug_base = slugify(unidecode(self.full_name))  # Преобразуем имя в слаг
            self.slug = slug_base

            # Проверяем уникальность слага и добавляем суффикс, если слаг уже существует
            counter = 1
            while City.objects.filter(slug=self.slug).exists():
                # Добавляем числовой суффикс, если слаг уже существует
                self.slug = f"{slug_base}-{counter}"
                counter += 1
        super().save(*args, **kwargs)