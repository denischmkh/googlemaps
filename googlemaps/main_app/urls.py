# urls.py
from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_page, name='account_signin'),
    path('register/', register_page, name='account_signup'),
    path('logout/', logout_user, name='logout'),
    path('<str:category>/', category_list_place_tm, name='category_list_place_tm'),
    path('info/<str:name_slug>/', place_full_info, name='place_full_info'),
]