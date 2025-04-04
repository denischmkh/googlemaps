from django.contrib import admin
from .models import Country, City, State, Category, Place

import data_wizard
data_wizard.register(Country)
data_wizard.register(City)
data_wizard.register(State)
data_wizard.register(Category)
data_wizard.register(Place)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "iso_code_2")
    search_fields = ("full_name", "iso_code_2")
    ordering = ("full_name",)
    list_filter = ("iso_code_2",)
    save_on_top = True

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ("id","full_name", "iso_code_2", "country")
    search_fields = ("full_name", "country__full_name")
    ordering = ("full_name",)
    list_filter = ("country",)
    autocomplete_fields = ("country",)
    save_on_top = True

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "country", "state")
    search_fields = ("full_name", "country__full_name", "state")
    ordering = ("full_name",)
    list_filter = ("country", "state")
    autocomplete_fields = ("country",)
    save_on_top = True

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)
    search_fields = ("name",)
    ordering = ("name",)
    save_on_top = True

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "city", "postcode", "rating", "status", "created_at")
    search_fields = ("name", "city", "category")
    list_filter = ("category", "status")
    ordering = ("-created_at",)
    # Убираем поля category и city из autocomplete_fields, так как они не являются ForeignKey
    autocomplete_fields = []  # Пустой список, так как autocomplete_fields не применяется к CharField
    readonly_fields = ("created_at", "clear_website")
    save_on_top = True
    list_select_related = ("category", "city", "city__country")

    fieldsets = (
        ("General Info", {
            "fields": ("name", "category", "about")
        }),
        ("Location", {
            "fields": ("city", "postcode", "full_address", "address", "located_in", "lat", "lng")
        }),
        ("Contact Info", {
            "fields": ("phone", "email", "website", "clear_website")
        }),
        ("Social Media", {
            "fields": ("facebook", "instagram", "linkedin", "youtube", "twitter")
        }),
        ("Ratings & Reviews", {
            "fields": ("rating", "num_reviews", "reviews_list")
        }),
        ("Operating Hours", {
            "fields": ("open_hours", "open_24_7")
        }),
        ("Status & Meta", {
            "fields": ("status", "link", "created_at")
        }),
    )