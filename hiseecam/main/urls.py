from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('ordering/', ordering, name='ordering'),
    path('search/', search, name='search')
]