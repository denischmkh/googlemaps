import ast
import json
from json import JSONDecodeError
from pprint import pprint

from django.shortcuts import render
from ..models import *

from django.http import JsonResponse

def index(request):
    category_names = Category.objects.all()

    for category in category_names:
        category.save()

    context = {"categories": category_names}
    return render(request, 'index.html', context)

from django.core.paginator import Paginator
from django.db.models import Count
def categoty_list_place_tm(request):
    page_number = request.GET.get("page", 1)
    items_per_page = 25
    
    # Получаем фильтры
    state_filter = request.GET.get("state", "")
    city_filter = request.GET.get("city", "")
    postcode_filter = request.GET.get("postcode", "")
    country_filter = request.GET.getlist("country")  # Получаем список выбранных стран
    category_filter = request.GET.getlist("category")
    print(category_filter)
    

    countries = Country.objects.all().order_by("full_name")

    # Получаем все категории для чекбоксов
    categories = Category.objects.annotate(
        place_count=Count('places')
    ).filter(place_count__gt=0).order_by("name")

    # Начинаем с получения всех мест
    places = Place.objects.all()

    # Применяем фильтры
    if category_filter:
        places = places.filter(category__slug__in=category_filter)

    if country_filter:
        places = places.filter(city__country__slug__in=country_filter)

    if state_filter:
        places = places.filter(city__state__full_name__icontains=state_filter)
    
    if city_filter:
        places = places.filter(city__full_name__icontains=city_filter)
    
    if postcode_filter:
        places = places.filter(postcode__icontains=postcode_filter)

    # Пагинация
    paginator = Paginator(places, items_per_page)
    page_obj = paginator.get_page(page_number)

    context = {
        "places": page_obj,
        "state_filter": state_filter,
        "city_filter": city_filter,
        "postcode_filter": postcode_filter,
        "country_filter": country_filter,
        "category_filter": category_filter[0].capitalize(),
        "categories": categories,
        "countries": countries,
    }
    return render(request, 'list_place.html', context)


def place_full_info(request, name_slug):
    place_obj = Place.objects.get(slug=name_slug)
    try:
        about = json.loads(place_obj.about)

        parsed_items = []
        for item in about:
            if ':' in item:
                key, value_str = item.split(':', 1)
                try:
                    values = ast.literal_eval(value_str.strip())
                    parsed_items.append({
                        'title': key.strip(),
                        'values': values
                    })
                except Exception:
                    parsed_items.append({
                        'title': key.strip(),
                        'values': [value_str.strip()]
                    })
    except (JSONDecodeError, AttributeError, TypeError):
        parsed_items = []
    try:
        open_hours = json.loads(place_obj.open_hours.replace("'", '"'))
    except (JSONDecodeError, AttributeError, TypeError):
        open_hours = {}

    context = {"place_obj": place_obj,
               'parsed_about': parsed_items,
               'open_hours': open_hours}
    return render(request, 'full_info2.html', context)