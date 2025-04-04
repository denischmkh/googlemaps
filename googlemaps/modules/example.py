import csv
import os
import random
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

os.environ['DJANGO_SETTINGS_MODULE'] = 'home_radar_project.settings'

import django
django.setup()

from agents_app.models import Agent, Company

for i in range(6, 9):
    print(i)
    csv_file_path = f'agents_{i}.csv'

    companies = list(Company.objects.all())

    agents_to_create = []

    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row.get('agent_name', '').strip()
            photo_url = row.get('agent_photo_url', '').strip()
            about = row.get('agent_about', '').strip()

            random_company = random.choice(companies)

            agent = Agent(
                name=name,
                company=random_company,
                about=about,
                phone=row.get('agent_phone_1', ''),
                listings=random.randint(0, 999),
                reviews=random.randint(0, 999),
                viewed=random.randint(0, 999),
                photo_url=photo_url,
                rating=random.randint(1, 5),
                facebook_url=random.choice([f"https://www.facebook.com/{name}", None]),
                twitter_url=random.choice([f"https://twitter.com/{name}", None]),
                instagram_url=random.choice([f"https://www.instagram.com/{name}", None]),
                vk_url=random.choice([f"https://vk.com/{name}", None]),
                is_verified=random.choice([True, False]),
                background_photo_url='',
            )

            agents_to_create.append(agent)

            if len(agents_to_create) >= 10000:
                Agent.objects.bulk_create(agents_to_create)
                print(f'Создано {len(agents_to_create)} агентов')
                agents_to_create.clear()

    if agents_to_create:
        Agent.objects.bulk_create(agents_to_create)
        print(f'Создано {len(agents_to_create)} агентов')