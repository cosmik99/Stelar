# C:\Django\Stelar\Stelar\store\views\cart.py

from django.shortcuts import render
from django.views import View
from core.models import Products # Necesitas Products para obtener los detalles de los items del carrito

# La clase debe llamarse EXACTAMENTE 'Cart' para que urls.py pueda importarla.
class Cart(View):
    def get(self, request):
        # 1. Obtener los IDs de los productos almacenados en la sesión (el carrito)
        ids = list(request.session.get('cart', {}).keys())
        
        # 2. Obtener los objetos Products correspondientes a esos IDs
        #    (Asumiendo que tienes un método get_products_by_id en tu models.py)
        products = Products.get_products_by_id(ids)
        
        # 3. Renderizar la plantilla del carrito
        return render(request, 'store/cart.html', {'products': products})

    # Si usas el método POST para actualizar cantidades o eliminar items
    def post(self, request):
        # ... Aquí iría la lógica para manejar el formulario del carrito (actualizar/eliminar)
        return self.get(request)