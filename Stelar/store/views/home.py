from django.shortcuts import render, redirect
from django.views import View

# 🟢 Importación relativa (asumimos que resuelve el error anterior)
from ..models import Product, Category 


def store(request):
    """
    Maneja la vista de la tienda, incluyendo el filtrado por categoría 
    y el procesamiento de datos del carrito para el resumen.
    """
    
    request.session.setdefault('cart', {}) 
    
    # --- Lógica de filtrado de productos ---
    products = None 
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    
    if categoryID:
        try:
            categoryID = int(categoryID)
            products = Product.get_all_products_by_categoryid(categoryID)
        except ValueError:
            products = Product.get_all_products()
    else:
        products = Product.get_all_products()

    # --- Lógica de PROCESAMIENTO del Carrito para el Resumen (AÑADIDA) ---
    cart = request.session.get('cart', {})
    items = []
    total = 0

    if cart:
        # Aquí falló antes porque Product era None
        products_in_cart = Product.objects.filter(id__in=cart.keys())

        for product in products_in_cart:
            quantity = cart.get(str(product.id))
            if quantity:
                subtotal = product.price * quantity
                items.append({
                    'product': product,
                    'quantity': quantity,
                    'get_total': subtotal,
                })
                # 🟢 CORRECCIÓN CLAVE: Mover la suma del total dentro del 'if'
                total += subtotal 

    order = {
        'get_cart_total': total,
        'get_cart_items': sum(item['quantity'] for item in items),
    }
    # ----------------------------------------------------------------------
    
    data = {
        'products': products,
        'categories': categories,
        'items': items, 
        'order': order,
    }

    print('Usuario logueado: ', request.session.get('customer_email'))
    return render(request, 'index.html', data)