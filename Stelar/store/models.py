# store/models.py
from django.db import models
import datetime


# --- MODELO CATEGORY ---
class Category(models.Model):
    name = models.CharField(max_length=50)

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    def __str__(self):
        return self.name


# --- MODELO CUSTOMER ---
class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def register(self):
        """Guarda un nuevo cliente."""
        self.save()

    @staticmethod
    def get_customer_by_email(email):
        """Obtiene un cliente por su correo electrónico."""
        try:
            return Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            return None

    def isExists(self):
        """Verifica si el cliente ya existe por su correo."""
        return Customer.objects.filter(email=self.email).exists()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# --- MODELO PRODUCT ---
class Product(models.Model):
    name = models.CharField(max_length=60)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=250, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/products/', blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        """
        Devuelve la URL válida de la imagen del producto.
        Si no hay imagen, devuelve un placeholder.
        """
        try:
            return self.image.url
        except:
            return 'https://via.placeholder.com/200x200.png?text=Sin+Imagen'

    @staticmethod
    def get_products_by_id(ids):
        """Obtiene una lista de productos por sus IDs."""
        return Product.objects.filter(id__in=ids)

    @staticmethod
    def get_all_products():
        """Obtiene todos los productos."""
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        """Filtra productos por categoría."""
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_products()


# --- MODELO ORDER ---
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=100, default='', blank=True)
    phone = models.CharField(max_length=20, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"Orden #{self.id} - {self.product.name}"

    def placeOrder(self):
        """Guarda la orden en la base de datos."""
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        """Obtiene todas las órdenes de un cliente específico."""
        return Order.objects.filter(customer=customer_id).order_by('-date')
