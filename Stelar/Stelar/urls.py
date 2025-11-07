from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

# 🟢 SOLUCIÓN: Usamos la importación estándar de settings de Django.
# Ya que este archivo está en la carpeta de configuración (Stelar), es seguro usar esto.
from django.conf import settings 

urlpatterns = [
    path('admin/', admin.site.urls),
    # Incluye todas las rutas de la aplicación 'store'
    path('', include('store.urls')),
]

# Configuración de archivos estáticos y de medios (MEDIA)
# La condición 'if settings.DEBUG:' es fundamental para esto.
if settings.DEBUG:
    # Media files (archivos subidos por el usuario)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Static files (CSS, JS, imágenes del proyecto)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)