from django.contrib import admin
from .models import Category, Customer, Order, Product 
# Si el nombre de tu modelo es 'Productss' o 'Categorys', cámbialo aquí.

# 1. Registrar el modelo Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',) # Muestra el nombre en la lista de administración
    # Puedes añadir más opciones si lo deseas

# 2. Registrar el modelo Customer
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'email', 'phone')

# 3. Registrar el modelo Order
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'date')

# 4. Registrar el modelo Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')