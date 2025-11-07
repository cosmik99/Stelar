# store/urls.py

from django.urls import path
from django.views.generic.base import RedirectView

from .views.home import store
from .views.signup import Signup
from .views.login import Login, logout_user
from .views.cart import CartHandler, Cart 
from .views.checkout import CheckOut
from .views.orders import OrderView
from .views.profile import Profile
from .views.search import search_view


urlpatterns = [
    # Ruta principal que redirige a 'store'
    path('', RedirectView.as_view(pattern_name='store', permanent=False), name='index'), 
    
    # Rutas de la tienda
    path('tienda/', store, name='store'),
    
    # Rutas de autenticación
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', logout_user, name='logout'), # Si tienes una vista de logout
    
    # Rutas del carrito (CartHandler maneja el POST, Cart maneja el GET)
    path('cart/', Cart.as_view(), name='cart'),
    path('cart-action/', CartHandler.as_view(), name='cart-action'),
    
    # Rutas de compra y órdenes
    path('checkout/', CheckOut.as_view(), name='checkout'),
    path('orders/', OrderView.as_view(), name='orders'), # Si tienes OrderView
    
    # Ruta de perfilA
    path('profile/', Profile.as_view(), name='profile'), # Si tienes Profile
    path('search/', search_view, name='search')
]
