from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.views import View
from store.models import Product, Order, Customer
#import json

class CheckOut(View):
    # --- MÉTODO GET: Muestra la página de Checkout (Formulario y Resumen) ---
    def get(self, request):
        # 1. Obtener la información del carrito desde la sesión
        cart = request.session.get('cart')
        if not cart:
            # Si el carrito está vacío, redirige al carrito/tienda
            return redirect('cart') 

        # 2. Obtener los productos basados en las claves del carrito
        product_ids = list(cart.keys())
        products = Product.get_products_by_id(product_ids)

        # 3. Calcular los ítems y el total para la plantilla
        # Nota: Adaptar esta lógica si usas OrderItem en lugar de Order directamente
        items_data = []
        total_price = 0
        
        for product in products:
            quantity = cart.get(str(product.id))
            price = product.price
            total = price * quantity
            total_price += total
            
            items_data.append({
                'product': product,
                'quantity': quantity,
                'get_total': total # Campo simulado para el total del ítem
            })

        # Prepara un objeto 'order' simple para el total de la plantilla
        order_summary = {
            'get_cart_total': total_price,
            'get_cart_items': len(product_ids)
        }
        
        context = {
            'items': items_data,
            'order': order_summary
        }
        
        # 4. Renderiza la plantilla (el botón 'Pagar Ahora' llama a este método)
        return render(request, 'store/checkout.html', context)


    # --- MÉTODO POST: Procesa el pago y guarda la Orden ---
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer_id = request.session.get('customer') # Renombré 'customer' a 'customer_id' para mayor claridad
        cart = request.session.get('cart')
        
        # Seguridad básica: Asegura que todos los datos estén presentes
        if not all([address, phone, customer_id, cart]):
            # Puedes añadir un mensaje de error aquí
            return redirect('cart') 

        products = Product.get_products_by_id(list(cart.keys()))
        
        # El resto de tu lógica POST es correcta para guardar la orden:
        for product in products:
            quantity = cart.get(str(product.id))
            
            # Crea y guarda cada artículo como una orden separada
            order = Order(customer=Customer(id=customer_id),
                product=product,
                price=product.price, # Nota: es mejor usar price * quantity en la vista de carrito
                address=address,
                phone=phone,
                quantity=quantity)
            order.save()
            
        # Limpiar el carrito de la sesión
        request.session['cart'] = {}

        # Redirigir al carrito o a una página de confirmación
        return redirect('cart')