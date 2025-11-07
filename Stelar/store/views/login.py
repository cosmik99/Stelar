# store/views/login.py
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.views import View
from store.models import Customer
from store.forms import LoginForm

class Login(View):
    def get(self, request):
        
        if request.session.get('customer_id'):
            return redirect('profile')

        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        error_message = None

        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            try:
                customer = Customer.objects.get(email=email)
            except Customer.DoesNotExist:
                customer = None

            if customer:
               
                if check_password(password, customer.password):
                    
                    request.session['customer_id'] = customer.id
                    request.session['customer_email'] = customer.email
                    print("✅ Sesión iniciada:", customer.email)
                    return redirect('profile')
                else:
                    error_message = '⚠️ Contraseña incorrecta.'
            else:
                error_message = '⚠️ El correo no está registrado.'
        else:
            error_message = '⚠️ Por favor completa todos los campos correctamente.'

        
        print("❌ Error de login:", error_message)
        return render(request, 'login.html', {'form': form, 'error': error_message})
