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
from .views.product_detail import product_detail


urlpatterns = [
    # --- Ruta principal ---
    path('', RedirectView.as_view(pattern_name='store', permanent=False), name='index'),
    
    # --- Tienda principal ---
    path('tienda/', store, name='store'),

    # --- Autenticación ---
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),

    # --- Carrito ---
    path('cart/', Cart.as_view(), name='cart'),
    path('cart-action/', CartHandler.as_view(), name='cart-action'),

    # --- Compras y órdenes ---
    path('checkout/', CheckOut.as_view(), name='checkout'),
    path('orders/', OrderView.as_view(), name='orders'),

    # --- Perfil de usuario ---
    path('profile/', Profile.as_view(), name='profile'),

    # --- Búsqueda ---
    path('search/', search_view, name='search'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
]
