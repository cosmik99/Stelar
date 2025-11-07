# store/urls.py

from django.contrib import admin
from django.urls import path
from django.views.generic.base import RedirectView
from django.shortcuts import redirect

# Vistas importadas
from .views.home import Index, store
from .views.signup import Signup
from .views.login import Login
from .views.cart import Cart
from .views.checkout import CheckOut
from .views.orders import OrderView
from .middlewares.auth import auth_middleware
from .views.search import search_view
from .views.profile import Profile

# Vista de logout como función
def logout(request):
    request.session.clear()
    return redirect('login')

urlpatterns = [
    # Redirección de raíz a tienda
    path('', RedirectView.as_view(pattern_name='store', permanent=False), name='index'),

    # Rutas principales
    path('tienda/', store, name='store'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', logout, name='logout'),
    path('cart/', Cart.as_view(), name='cart'), # elimine esto auth_middleware
    path('check-out/', CheckOut.as_view(), name='checkout'),
    path('orders/', OrderView.as_view(), name='orders'), # elimine esto auth_middleware
    path('search/', search_view, name='search'),
    path('profile/', Profile.as_view(), name='profile'),
]
