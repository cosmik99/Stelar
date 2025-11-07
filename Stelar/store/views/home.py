# store/views/home.py

from django.shortcuts import render, redirect
# Asegúrate de importar Products y Category desde donde estén definidos
from core.models import Products, Category 
from django.views import View

def store(request):
    """
    Maneja la vista de la tienda, incluyendo el filtrado por categoría 
    y el procesamiento de datos del carrito para el resumen.
    """
    
    request.session.setdefault('cart', {}) 
    
    # --- Lógica de filtrado de productos (Se mantiene igual) ---
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    
    if categoryID:
        try:
            categoryID = int(categoryID)
            products = Products.get_all_products_by_categoryid(categoryID)
        except ValueError:
            products = Products.get_all_products()
    else:
        products = Products.get_all_products()

    # --- Lógica de PROCESAMIENTO del Carrito para el Resumen (AÑADIDA) ---
    cart = request.session.get('cart', {})
    items = []
    total = 0

    if cart:
        # Importante: Obtener solo los productos cuyos IDs están en el carrito
        products_in_cart = Products.objects.filter(id__in=cart.keys())

        for product in products_in_cart:
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
    # ----------------------------------------------------------------------
    
    data = {
        'products': products,
        'categories': categories,
        'items': items,    # <-- CLAVE: Los ítems procesados
        'order': order,    # <-- CLAVE: Los totales
    }

    print('Usuario logueado: ', request.session.get('customer_email'))
    # Asumimos que el template principal es 'index.html'
    return render(request, 'index.html', data)