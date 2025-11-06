from django.urls import path
from . import views  # Importa las vistas (views.py) de esta misma carpeta

urlpatterns = [
    # Cuando alguien visite la URL 'store/' (que ya definimos en el paso A),
    # esta regla se encarga del resto del camino.
    # Como el camino está vacío (''), ejecutará la vista 'store'.
    path('', views.store, name='store'),
]