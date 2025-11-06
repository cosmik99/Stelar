# C:\Django\Stelar\Stelar\store\middlewares\auth.py

from django.shortcuts import redirect

def auth_middleware(get_response):
    """
    Middleware que asegura que un usuario esté logueado (verificando la sesión 'customer').
    Si el usuario no está logueado, lo redirige a la página de login.
    """
    
    # Esta parte (fuera de 'middleware') es el código de inicialización.
    # Se ejecuta una vez al iniciar el servidor.
    
    def middleware(request):
        # Esta parte se ejecuta ANTES de la vista.
        
        # Lista de URLs que no requieren autenticación (excepciones)
        # Esto es crucial para que el usuario pueda acceder al login.
        excluded_urls = [
            '/login',
            '/signup',
            # Añade aquí otras URLs públicas si las tienes, como '/contacto' o '/acerca-de'
        ]
        
        # Verifica si el camino actual requiere autenticación y si el usuario no tiene la sesión.
        # Usa request.path_info para obtener la ruta sin el dominio.
        if request.path_info not in excluded_urls and not request.session.get('customer'):
            # Redirige a la página de login
            return redirect('login') 
        
        # Si está autenticado o la URL es una excepción, pasa la solicitud a la vista
        response = get_response(request)
        
        # Esta parte se ejecuta DESPUÉS de la vista.
        
        return response

    return middleware