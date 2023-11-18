from django.urls import path
from mapa.views import index, svg_to_graph

urlpatterns = [
    path('', index, name='index'),
    path('svg_to_graph/', svg_to_graph, name='svg_to_graph'),
]