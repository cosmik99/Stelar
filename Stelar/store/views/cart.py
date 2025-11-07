# store/views/cart.py
from django.shortcuts import render, redirect
from django.views import View
from core.models import Products  

class Cart(View):
    def get(self, request):
        
        cart = request.session.get('cart', {})

        items = []
        total = 0

       
        if cart:
            
            products = Products.objects.filter(id__in=cart.keys())

            for product in products:
                quantity = cart[str(product.id)]
                subtotal = product.price * quantity

                items.append({
                    'product': product,
                    'quantity': quantity,
                    'get_total': subtotal,
                })

                total += subtotal

        
        order = {
            'get_cart_total': total,
            'get_cart_items': sum(item['quantity'] for item in items),
        }

        context = {
            'items': items,
            'order': order,
        }

        return render(request, 'cart.html', context)
    
# 🚀 ADICIÓN DEL MÉTODO POST (Necesario para romper el bucle) 🚀
    def post(self, request):
        
        # Aunque esta función debería manejar la lógica de actualizar la sesión
        # al usar los botones de añadir/quitar del carrito...
        
        # Por ahora, solo necesitamos asegurarnos de que la vista POST exista
        # y use la redirección correcta para seguir el patrón PRG (Post/Redirect/Get),
        # lo cual es crucial para evitar el bucle.
        
        return redirect('cart')
