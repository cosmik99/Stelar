from django.shortcuts import render, redirect
from django.views import View
from store.models import Product
from django.contrib import messages  


# --- 1. Vista para MOSTRAR el carrito (GET /cart/) ---
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


# --- 2. Vista para MANEJAR la acción de agregar/quitar/eliminar (POST /cart-action/) ---
class CartHandler(View):
    """
    Se encarga de la lógica POST para agregar, quitar o eliminar productos del carrito.
    """

    def post(self, request):
        product_id = request.POST.get('product')
        remove = request.POST.get('remove') == 'True'
        delete_all = request.POST.get('delete_all') == 'True'  

        cart = request.session.get('cart', {})

        if product_id:
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                messages.error(request, "El producto no existe.")
                return redirect('cart')

            product_id = str(product_id)
            quantity = cart.get(product_id, 0)

            # 🔴 Validación de stock
            if not remove and not delete_all:
                if product.stock == 0:
                    messages.warning(request, f"❌ El producto '{product.name}' está agotado.")
                    return redirect('cart')

                if quantity >= product.stock:
                    messages.warning(request, f"Solo quedan {product.stock} unidades disponibles de '{product.name}'.")
                    return redirect('cart')

            # 🔁 Lógica normal del carrito
            if delete_all:
                # 🧨 Eliminar completamente el producto del carrito
                if product_id in cart:
                    cart.pop(product_id)
                    messages.warning(request, "Producto eliminado del carrito.")
            elif remove:
                # ➖ Disminuir cantidad
                if quantity > 1:
                    cart[product_id] = quantity - 1
                elif quantity == 1:
                    cart.pop(product_id)
                    messages.info(request, "Producto eliminado del carrito.")
            else:
                # ➕ Aumentar cantidad
                cart[product_id] = quantity + 1
                messages.success(request, "Producto agregado al carrito.")

            # 🧠 Guardar los cambios
            request.session['cart'] = cart
            request.session.modified = True

        print('🛒 Cart actualizado:', request.session.get('cart'))

        # ✅ Redirige al carrito (no a la tienda)
        return redirect('cart')
