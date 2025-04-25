# urls.py
from django.urls import path

from .views import *

urlpatterns = [
    # Basic
    path('', index, name='index'),
    path('places/list/', categoty_list_place_tm, name='categoty_list_place_tm'),
    path('info/<str:name_slug>/', place_full_info, name='place_full_info'),
    path('agents/', get_agents, name='get_agents')
]