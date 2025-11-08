# store/views/product_detail.py
from django.shortcuts import render, get_object_or_404
from store.models import Product

def product_detail(request, product_id):
    """
    Muestra los detalles de un producto específico.
    """
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

