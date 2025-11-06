from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.views import View
# Importar el decorador
from django.utils.decorators import method_decorator 

from core.models import Order
from store.middlewares.auth import auth_middleware


class OrderView(View):
    # Aplicar el decorador al método 'get' usando el middleware importado
    @method_decorator(auth_middleware)
    def get(self, request):
        # Esta línea ya no es necesaria, el middleware se encarga de esto:
        # customer = request.session.get('customer') 
        
        # El middleware DEBERÍA asegurarse de que 'customer' exista en la sesión 
        # o de que ya se haya redirigido, pero para ser más robustos, lo puedes obtener
        customer = request.session.get('customer') 
        
        orders = Order.get_orders_by_customer(customer)
        print(orders)
        return render(request, 'orders.html', {'orders': orders})

# NOTA: Si tu middleware ya asigna el ID del cliente a request.customer 
# o similar, entonces puedes simplificar aún más.