from django.db import models

from django.utils.text import slugify
from unidecode import unidecode

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name="Category Name")
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True, verbose_name="Category Slug")
    icon = models.CharField(null=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # Транслитерируем кириллицу в латиницу
            slug_base = slugify(unidecode(self.name))  # Преобразуем имя в слаг
            self.slug = slug_base

            # Проверяем уникальность слага и добавляем суффикс, если слаг уже существует
            counter = 1
            while Category.objects.filter(slug=self.slug).exists():
                # Добавляем числовой суффикс, если слаг уже существует
                self.slug = f"{slug_base}-{counter}"
                counter += 1
        super().save(*args, **kwargs)