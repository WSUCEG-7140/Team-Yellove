from django.urls import path   # for urls: https://docs.djangoproject.com/en/4.2/ref/urls/
from authentication.views import create_user, get_user_list

urlpatterns = [
    path('users/', create_user, name='create_user'),
    path('users/list/', get_user_list, name='get_user_list')
]

from django.urls import path
from authentication.views import create_user, get_user_list
