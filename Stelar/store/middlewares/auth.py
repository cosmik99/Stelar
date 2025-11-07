from django.shortcuts import redirect
from django.urls import reverse

def auth_middleware(get_response):
    # Rutas que NO requieren autenticación
    EXCLUDE_PATHS = ['/login/', '/signup/']

    def middleware(request):
        is_authenticated = request.session.get('customer_id') 
        current_path = request.path

        # 1. Chequea si el usuario NO está logueado
        if not is_authenticated:
            # 2. Chequea si la ruta actual NO es una ruta excluida (login o signup)
            # Nota: Usamos startswith() para cubrir casos como /login/?return_url=...
            is_excluded = any(current_path.startswith(path) for path in EXCLUDE_PATHS)
            
            if not is_excluded:
                # 3. Redirige a la página de login, pasando la URL actual como return_url
                # Usamos reverse() para obtener la URL 'login' por su nombre, garantizando que existe.
                login_url = reverse('login')
                return redirect(f'{login_url}?return_url={current_path}')
        
        return get_response(request)
    return middleware