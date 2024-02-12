from django.urls import path
from .views import hello_world, setup, searchQuery, predictIndex, predictCategory

urlpatterns = [
    path('', hello_world, name='hello_world'),
    path('setup', setup, name='setup'),
    path('search', searchQuery, name='search'),
    path('predict_index', predictIndex, name='predict_index'),
    path('predict_make', predictCategory, name='predict_make')
]
