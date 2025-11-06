# C:\Django\Stelar\Stelar\store\models.py

from django.db import models
import datetime
from django.contrib.auth.hashers import make_password, check_password 


# ====================================================================
# 1. Modelo Category (Categoría)
# ====================================================================

class Category(models.Model):
    name = models.CharField(max_length=50)

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    def __str__(self):
        return self.name

# ====================================================================
# 2. Modelo Customer (Cliente)
# ====================================================================

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    password = models.CharField(max_length=100)

    def register(self):
        self.save()

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            return False

    def isExists(self):
        return Customer.objects.filter(email=self.email).exists()

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'


# ====================================================================
# 3. Modelo Products (Productos) - ¡Nombre crucial para la importación!
# ====================================================================

class Products(models.Model):
    name = models.CharField(max_length=60)
    price = models.IntegerField(default=0)
    # FK a Category
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1) 
    description = models.CharField(
        max_length=250, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/products/') 

    @staticmethod
    def get_products_by_id(ids):
        return Products.objects.filter(id__in=ids)

    @staticmethod
    def get_all_products(category_id=None):
        if category_id:
            return Products.objects.filter(category=category_id)
        return Products.objects.all()

    def __str__(self):
        return self.name


# ====================================================================
# 4. Modelo Order (Pedido)
# ====================================================================

class Order(models.Model):
    # FK a Products (usa la clase definida arriba)
    product = models.ForeignKey(Products, on_delete=models.CASCADE) 
    # FK a Customer (usa la clase definida arriba)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField() 
    address = models.CharField(max_length=50, default='', blank=True)
    phone = models.CharField(max_length=50, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False) 

    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-date')

    def __str__(self):
        return f'Order #{self.id} by {self.customer.first_name} for {self.product.name}'