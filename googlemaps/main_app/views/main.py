import ast
import json
from json import JSONDecodeError
from pprint import pprint
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout as auth_logout

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from ..forms import LoginForm, SignupForm
from ..models import *

from django.http import JsonResponse


def index(request):
    category_names = Category.objects.all()

    for category in category_names:
        category.save()

    countries = Country.objects.all().order_by("full_name")

    context = {"categories": category_names,
               "countries": countries,
               'selected_category': 'All Categories'}
    return render(request, 'index.html', context)


from django.core.paginator import Paginator
from django.db.models import Count


def category_list_place_tm(request, category=None):
    if category is None:
        category = 'all'
    page_number = request.GET.get("page", 1)
    items_per_page = 25

    state_filter = request.GET.get("state", "")
    city_filter = request.GET.get("city", "")
    postcode_filter = request.GET.get("postcode", "")
    country_filter = [slugify(el) for el in request.GET.getlist("country")]  # Получаем список выбранных стран
    category_filter = [category]
    category_filter[0] = slugify(category_filter[0])
    keywords_filter = request.GET.get("keywords")

    countries = Country.objects.all().order_by("full_name")

    # Получаем все категории для чекбоксов
    categories = Category.objects.annotate(
        place_count=Count('places')
    ).filter(place_count__gt=0).order_by("name")

    # Начинаем с получения всех мест
    places = Place.objects.all()

    # Применяем фильтры
    if category_filter[0] != 'all-categories':
        places = places.filter(category__slug__in=category_filter)

    if country_filter:
        places = places.filter(city__country__slug__in=country_filter)

    if state_filter:
        places = places.filter(city__state__full_name__icontains=state_filter)

    if city_filter:
        places = places.filter(city__full_name__icontains=city_filter)

    if postcode_filter:
        places = places.filter(postcode__icontains=postcode_filter)

    if keywords_filter:
        places = places.filter(name__icontains=keywords_filter)

    # Пагинация
    paginator = Paginator(places, items_per_page)
    page_obj = paginator.get_page(page_number)
    print(category_filter)

    if category_filter[0] != 'all-categories':
        selected_category = Category.objects.filter(slug=slugify(category_filter[0])).first()
        selected_category_name = selected_category.name
        selected_category = selected_category.slug

    else:
        selected_category = 'all-categories'
        selected_category_name = 'All categories'

    context = {
        "places": page_obj,
        "state_filter": state_filter,
        "city_filter": city_filter,
        "postcode_filter": postcode_filter,
        "country_filter": country_filter,
        "selected_category": selected_category,
        'selected_category_name': selected_category_name,
        "categories": categories,
        "countries": countries,
        'category_filter': category_filter[0],
        'selected_country_unslug': Country.objects.filter(slug=country_filter[0]).first() if country_filter else None,
        'keywords_filter': keywords_filter
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
    countries = Country.objects.all().order_by("full_name")

    context = {"place_obj": place_obj,
               'parsed_about': parsed_items,
               'open_hours': open_hours,
               'selected_category': slugify(place_obj.category.slug),
               'selected_category_name': place_obj.category.name,
               'category_filter': place_obj.category.slug,
               'name': place_obj.name,
               "countries": countries,
               }
    return render(request, 'full_info3.html', context)


def login_page(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']  # исправлено с 'login'
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            form.add_error(None, 'Invalid username or password.')
    return render(request, 'account/login.html', {'form': form})

def register_page(request):
    form = SignupForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password1 = form.cleaned_data['password1']
        password2 = form.cleaned_data['password2']

        if password1 != password2:
            form.add_error('password2', 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            form.add_error('username', 'Username already taken.')
        elif User.objects.filter(email=email).exists():
            form.add_error('email', 'Email already used.')
        else:
            user = User.objects.create(
                username=username,
                email=email,
                password=make_password(password1)
            )
            login(request, user)
            return redirect('index')

    return render(request, 'account/signup.html', {'form': form})

def logout_user(request):
    auth_logout(request)
    return redirect('index')