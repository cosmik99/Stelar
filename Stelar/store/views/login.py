# store/views/login.py

from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.hashers import check_password
from core.models import Customer
from django.views import View
# Asegúrate de que LoginForm esté definido e importado correctamente
from ..forms import LoginForm 


class Login(View):
    return_url = None

    def get(self, request):
        # 🚨 CAMBIO CRÍTICO: Instanciar y pasar el formulario para el renderizado
        form = LoginForm()
        Login.return_url = request.GET.get('return_url')
        
        # Pasar el formulario al contexto
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        # 1. Instanciar el formulario con los datos POST
        form = LoginForm(request.POST) 
        error_message = None

        if form.is_valid():
            # 2. Obtener datos limpios del formulario (en lugar de request.POST.get)
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            
            customer = Customer.get_customer_by_email(email)

            if customer:
                flag = check_password(password, customer.password)
                if flag:
                    request.session['customer'] = customer.id

                    if Login.return_url:
                        return HttpResponseRedirect(Login.return_url)
                    else:
                        Login.return_url = None
                        return redirect('homepage')
                else:
                    error_message = 'Invalid email or password.'
            else:
                error_message = 'Invalid email or password.'
        
        # Si el formulario no es válido o hay un error de autenticación:
        # 3. Renderizar la plantilla, pasando el formulario (que contiene errores) 
        # y el mensaje de error manual (si existe).
        context = {
            'form': form,
            'error': error_message
        }
        return render(request, 'login.html', context)


def logout(request):
    request.session.clear()
    return redirect('login')