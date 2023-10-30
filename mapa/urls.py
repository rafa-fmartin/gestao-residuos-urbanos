from django.urls import path
from mapa.views import index

urlpatterns = [
    path('', index, name='index'),
]