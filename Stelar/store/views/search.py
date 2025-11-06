from django.shortcuts import render
from django.db.models import Q
from ..models import Product  # Importa el modelo desde la carpeta raíz

def search_view(request):
    query = request.GET.get('q', '')
    results = []
    
    if query:
        results = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
    
    context = {
        'query': query,
        'results': results
    }

    return render(request, 'search_results.html', context)
