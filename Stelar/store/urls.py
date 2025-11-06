# store/urls.py

from django.contrib import admin
from django.urls import path
# 1. IMPORTA RedirectView
from django.views.generic.base import RedirectView 

# Tus imports de vistas
from .views.home import Index, store
from .views.signup import Signup
from .views.login import Login, logout
from .views.cart import Cart
from .views.checkout import CheckOut
from .views.orders import OrderView
from .middlewares.auth import auth_middleware


urlpatterns = [
    # 2. CAMBIA ESTA LÍNEA
    # Ahora la ruta raíz ('') redirige a la ruta con name='store'
    # Mantenemos name='index' para que otros enlaces no se rompan.
    path('', RedirectView.as_view(pattern_name='store', permanent=False), name='index'),

    # 3. ESTA ES LA RUTA DE DESTINO
    # (La vista 'store' se muestra en la URL '/tienda/')
    path('tienda/', store, name='store'),
    
    # --- El resto de tus rutas ---
    path('signup', Signup.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path('logout', logout, name='logout'),
    path('cart', auth_middleware(Cart.as_view()), name='cart'),
    path('check-out', CheckOut.as_view(), name='checkout'),
    path('orders', auth_middleware(OrderView.as_view()), name='orders'),
]