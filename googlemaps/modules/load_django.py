import os
import sys
from pprint import pprint

import django

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'googlemaps')))

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


django.setup()