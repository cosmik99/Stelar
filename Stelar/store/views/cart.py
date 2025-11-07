# store/views/cart.py (Versión Corregida)

from django.shortcuts import render, redirect
from django.views import View
from core.models import Products 

# --- 1. Vista para MOSTRAR el carrito (GET /cart/) ---
class Cart(View):
    def get(self, request):
        
        # El procesamiento de la lógica es CORRECTO para la página /cart/
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

        # Esto funciona bien si el template 'cart.html' usa 'items' y 'order'
        return render(request, 'cart.html', context)


# --- 2. Vista para MANEJAR la acción de agregar/quitar (POST /cart-action/) ---
# Esta clase debe estar aquí para que puedas importarla en urls.py
class CartHandler(View):
    """
    Se encarga exclusivamente de la lógica POST
    de agregar, quitar o actualizar productos del carrito.
    """
    def post(self, request):
        product_id = request.POST.get('product')
        remove = request.POST.get('remove') == 'True' 
        cart = request.session.get('cart', {})

        if product_id:
            product_id = str(product_id)
            quantity = cart.get(product_id, 0)
            
            if remove:
                if quantity > 0: 
                    cart[product_id] = quantity - 1
                    if cart[product_id] <= 0:
                        cart.pop(product_id)
            else:
                cart[product_id] = quantity + 1

            request.session['cart'] = cart
            # Siempre es vital marcar la sesión como modificada
            request.session.modified = True 
            
        print('Cart actualizado:', request.session['cart'])
        
        return_url = request.POST.get('return_url') or 'store'
        # Redirige para forzar la recarga de la página, lo que activa el GET
        return redirect(return_url)