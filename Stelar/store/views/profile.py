# store/views/profile.py
from django.shortcuts import render, redirect
from django.views import View
from store.models import Customer

class Profile(View):
    def get(self, request):
        
        customer_id = request.session.get('customer_id')

        if not customer_id:
            return redirect('login')

        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return redirect('login')

        return render(request, 'profile.html', {'customer': customer})

