import csv
import json
import re
import sys
from datetime import datetime

from django.db import IntegrityError

from load_django import *
from main_app.models.places import Place
from main_app.models.countries import Country, City, State
from main_app.models.categories import Category
import psycopg2





# Подключение к базе данных
connection = psycopg2.connect(
    dbname="vape_db",
    user="postgres",
    password="denis2004",
    host="localhost"
)



# Создание курсора

cursor = connection.cursor()
# Запрос к таблице
# for table in tables:
query = f"select * from place_vapeshop;"

# Выполнение запроса
cursor.execute(query)

# Получение названий столбцов (используем cursor.description)
column_names = [desc[0] for desc in cursor.description]

# Получение всех строк из таблицы
rows = cursor.fetchall()

for row in rows:
    row_dict = dict(zip(column_names, row))

    if 'id' in row_dict:
        del row_dict['id']

    pprint(row_dict)

    try:
        if bool(re.fullmatch(r'[A-Z]{2} \d{5}', row_dict.get('country'))):
            raise AttributeError
        else:
            country, created = Country.objects.get_or_create(full_name=row_dict['country'])

    except (AttributeError, TypeError, IntegrityError):
        country = None

    # Обработка штата
    try:
        if country:  # Проверяем, что country существует
            state, created = State.objects.get_or_create(
                full_name=row_dict.get('state'),
                country=country
            )
        else:
            state = None
    except (AttributeError, IntegrityError):
        state = None

    # Обработка города
    try:
        if country and len(row_dict.get('city')) != 0:
            city, created = City.objects.get_or_create(
                full_name=row_dict.get('city'),
                country=country,
                state=state if row_dict.get('state') else None
            )
        else:
            city = None
    except (AttributeError, IntegrityError, TypeError):
        city = None

    # Обработка категории
    try:
        category, created = Category.objects.get_or_create(
            name=row_dict.get('category')
        )
    except (AttributeError, IntegrityError):
        category = None

    # Пропуск, если нет имени
    if not row_dict.get('name') or row_dict.get('name') == '':
        print('No name')
        continue

    # Обработка почтового индекса
    try:
        postcode = int(row_dict.get('zip_code', None))
    except (TypeError, ValueError):
        postcode = None

    place = Place.objects.get_or_create(
        category=category,
        name=row_dict.get('name'),
        rating=float(row_dict.get('rating')) if row_dict.get('rating') else None,
        num_reviews=int(row_dict.get('num_reviews').replace(',', "")) if row_dict.get('num_reviews') else None,
        reviews_list=json.dumps(row_dict.get('reviews_list')) if row_dict.get('reviews_list') else None,
        about=row_dict.get('about', None),
        city=city,
        full_address=row_dict.get('full_address', None),
        address=row_dict.get('address', None),
        located_in=row_dict.get('located_in', None),
        postcode=postcode,
        lat=float(row_dict.get('lat')) if row_dict.get('lat') else None,
        lng=float(row_dict.get('lng')) if row_dict.get('lng') else None,
        place_type=row_dict.get('place_type', None),
        open_hours=row_dict.get('open_hours', None),
        open_24_7=True if row_dict.get('open_24_7') == 'Yes' else False,
        phone=row_dict.get('phone', None),
        email=row_dict.get('email').split(',')[0] if row_dict.get('email') else None,
        website=row_dict.get('website', None),
        clear_website=row_dict.get('clear_website', None),
        facebook=row_dict.get('facebook', None),
        linkedin=row_dict.get('linkedin', None),
        youtube=row_dict.get('youtube', None),
        twitter=row_dict.get('twitter', None),
        instagram=row_dict.get('instagram', None),
        link=row_dict.get('link', None),
        status=row_dict.get('status', None),
        created_at=row_dict.get('created_at', None)
    )

    # else:
    #     print(f"Skipping place due to missing category or city: {row_dict.get('name')}")


cursor.close()
connection.close()
