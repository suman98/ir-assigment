from django.urls import path
from .views import hello_world, setup, searchQuery

urlpatterns = [
    path('', hello_world, name='hello_world'),
    path('setup', setup, name='setup'),
    path('search', searchQuery, name='search')
]
