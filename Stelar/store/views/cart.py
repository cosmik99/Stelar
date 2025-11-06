# store/views/cart.py
from django.shortcuts import render
from django.views import View
from core.models import Products  # o store.models si ahí está tu modelo Product

class Cart(View):
    def get(self, request):
        # Obtenemos el carrito desde la sesión
        cart = request.session.get('cart', {})

        items = []
        total = 0

        # Si el carrito no está vacío
        if cart:
            # Obtener todos los productos cuyas IDs están en el carrito
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

        # Estructuramos un objeto order para compatibilidad con tu template
        order = {
            'get_cart_total': total,
            'get_cart_items': sum(item['quantity'] for item in items),
        }

        context = {
            'items': items,
            'order': order,
        }

        return render(request, 'cart.html', context)
