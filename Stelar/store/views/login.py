from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from store.models import Customer
from django.contrib.auth.hashers import check_password
from django.contrib.auth import logout


class Login(View):
    def get(self, request):
        """
        Muestra el formulario de inicio de sesión.
        Si ya hay un usuario logueado, redirige a la tienda.
        """
        if request.session.get('customer_id'):
            return redirect('store')

        return_url = request.GET.get('return_url')
        context = {'return_url': return_url}
        return render(request, 'login.html', context)

    def post(self, request):
        """
        Procesa el formulario de inicio de sesión.
        """
        email = request.POST.get('email')
        password = request.POST.get('password')
        return_url = request.POST.get('return_url')

        error_message = None

        print("📩 POST recibido:", email)

        # Buscar cliente en la base de datos
        customer = Customer.objects.filter(email=email).first()

        if customer:
            if check_password(password, customer.password):
                # ✅ Contraseña correcta
                request.session['customer_id'] = customer.id
                request.session['customer_email'] = customer.email
                print(f"✅ Sesión iniciada para: {customer.email}")

                messages.success(request, f"Bienvenido {customer.first_name}!")

                # Redirigir si había una URL de retorno, si no a la tienda
                if return_url:
                    return redirect(return_url)
                return redirect('store')

            else:
                error_message = "⚠️ Contraseña incorrecta."
                print("❌ Contraseña incorrecta.")
        else:
            error_message = "⚠️ El correo no está registrado."
            print("❌ Correo no encontrado.")

        context = {
            'error': error_message,
            'return_url': return_url,
            'email': email,
        }

        return render(request, 'login.html', context)


def logout_user(request):
    """
    Cierra la sesión del usuario actual.
    """
    logout(request)
    request.session.flush()
    messages.info(request, "Sesión cerrada correctamente.")
    return redirect('store')
