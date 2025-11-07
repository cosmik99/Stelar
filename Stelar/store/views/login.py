from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.views import View
from store.models import Customer
from store.forms import LoginForm
from django.contrib.auth import logout # Importar la función logout de Django
from django.contrib import messages # Para mostrar mensajes después del logout

# --- FUNCIÓN DE LOGOUT (NECESARIA PARA LA URL 'logout') ---
def logout_user(request):
    """
    Cierra la sesión del usuario actual (elimina customer_id y la sesión de Django) 
    y lo redirige a la página de inicio de la tienda.
    """
    # 1. Usar la función de logout de Django para limpiar la sesión
    logout(request) 
    
    # 2. Eliminar la custom key 'customer_id' si existe
    if 'customer_id' in request.session:
        del request.session['customer_id']
        
    # Opcional: Mostrar un mensaje
    messages.info(request, "Has cerrado sesión correctamente.")
    
    # 3. Redirigir a la tienda
    return redirect('store')

# --- VISTA DE LOGIN (EXISTENTE Y MODIFICADA) ---
class Login(View):
    def get(self, request):
        
        # 1. Si el usuario ya está logueado, redirige a la tienda.
        if request.session.get('customer_id'):
            return redirect('store')

        form = LoginForm()
        # Captura la 'return_url' del parámetro GET (si existe)
        return_url = request.GET.get('return_url')
        
        # Pasa el 'return_url' al contexto, para que pueda ser incluido 
        # como un campo oculto en el formulario de login.
        return render(request, 'login.html', {'form': form, 'return_url': return_url})

    def post(self, request):
        form = LoginForm(request.POST)
        error_message = None
        
        # --- Captura el destino de redirección ---
        # Si se envió un campo oculto 'return_url' en el POST, lo capturamos.
        post_data = request.POST
        return_url = post_data.get('return_url') # Captura el campo oculto

        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            try:
                customer = Customer.objects.get(email=email)
            except Customer.DoesNotExist:
                customer = None

            if customer:
                if check_password(password, customer.password):
                    
                    # 2. INICIO DE SESIÓN EXITOSO
                    request.session['customer_id'] = customer.id
                    request.session['customer_email'] = customer.email
                    print("✅ Sesión iniciada:", customer.email)
                    
                    # 3. LÓGICA DE REDIRECCIÓN CORREGIDA
                    # Redirige a la URL guardada (ej: '/cart/') si existe.
                    if return_url:
                        return redirect(return_url)
                    else:
                        return redirect('store') 
                    
                else:
                    error_message = '⚠️ Contraseña incorrecta.'
            else:
                error_message = '⚠️ El correo no está registrado.'
        else:
            error_message = '⚠️ Por favor completa todos los campos correctamente.'

        # En caso de fallo de login, se mantiene la return_url en el contexto.
        print("❌ Error de login:", error_message)
        return render(request, 'login.html', {'form': form, 'error': error_message, 'return_url': return_url})