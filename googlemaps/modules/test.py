from load_django import *
from main_app.models.places import Place
from main_app.models.countries import Country, City, State


country_names_to_delete = [
    "46000", "AR 7HMH+XC", "CA 9016", "CA91780邮政编码: 91780", "邮政编码: 92630"
]

# 1. Найти страны
countries = Country.objects.filter(full_name__in=country_names_to_delete)

# 2. Найти города в этих странах
cities = City.objects.filter(country__in=countries)

# 3. Удалить все Place, связанные с этими городами
Place.objects.filter(city__in=cities).delete()

# 4. Удалить города
cities.delete()

# 5. Удалить страны
countries.delete()

# 197432 Все места
# 172614 Только США