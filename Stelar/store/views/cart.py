from django.shortcuts import render, redirect
from django.views import View
from store.models import Product 


# --- 1. Vista para MOSTRAR el carrito (GET /cart/) ---
# Asegúrate de que esta clase comience al borde izquierdo.
class Cart(View):
    def get(self, request):
        
        cart = request.session.get('cart', {})
        items = []
        total = 0

        if cart:
            products = Product.objects.filter(id__in=cart.keys())

            for product in products:
                quantity = cart.get(str(product.id), 0)
                # 🟢 Aseguramos que la cantidad exista y sea positiva
                if quantity: 
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

# --- 2. Vista para MANEJAR la acción de agregar/quitar (POST /cart-action/) ---
# Asegúrate de que esta clase comience al borde izquierdo.
class CartHandler(View):
    """
    Se encarga de la lógica POST para agregar, quitar o actualizar productos del carrito.
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
            request.session.modified = True 
            
        print('Cart actualizado:', request.session.get('cart'))
        
        return_url = request.POST.get('return_url') or 'store'
        return redirect(return_url)