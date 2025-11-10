# store/models.py

from django.db import models
import datetime
from PIL import Image 
from io import BytesIO
from django.core.files.base import ContentFile
import os 


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
        self.save()

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            return None

    def isExists(self):
        return Customer.objects.filter(email=self.email).exists()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# --- MODELO PRODUCT (CON REDIMENSIONAMIENTO A TAMAÑO EXACTO Y RELLENO) ---
class Product(models.Model):
    name = models.CharField(max_length=60)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=250, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/products/', blank=True, null=True)

    # ---------------------------------------------------------------------
    # 🎉 LÓGICA DE REDIMENSIONAMIENTO A 250x250 CON RELLENO WHITESMOKE 🎉
    # ---------------------------------------------------------------------
    def save(self, *args, **kwargs):
        # 1. Guarda el modelo primero para que el archivo de imagen tenga una ruta (path)
        super().save(*args, **kwargs) 

        # 2. Verifica si se subió una imagen
        if self.image:
            img = Image.open(self.image.path)
            
            TARGET_WIDTH = 250
            TARGET_HEIGHT = 250
            TARGET_SIZE = (TARGET_WIDTH, TARGET_HEIGHT)
            FILL_COLOR = (245, 245, 245) # Color 'whitesmoke' en RGB

            # 3. Calcular la relación de aspecto de la imagen original
            original_width, original_height = img.size
            aspect_ratio = original_width / original_height

            # 4. Redimensionar la imagen para que quepa en el cuadrado de 250x250
            # manteniendo su proporción. Escala para que el lado más largo sea 250.
            if original_width > original_height:
                # La imagen es más ancha que alta, ajusta el ancho a 250
                new_width = TARGET_WIDTH
                new_height = int(new_width / aspect_ratio)
            else:
                # La imagen es más alta que ancha (o cuadrada), ajusta el alto a 250
                new_height = TARGET_HEIGHT
                new_width = int(new_height * aspect_ratio)

            # Redimensiona la imagen al tamaño calculado
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # 5. Crear un nuevo lienzo de 250x250 con el color de fondo
            canvas = Image.new('RGB', TARGET_SIZE, color=FILL_COLOR)

            # 6. Calcular la posición para pegar la imagen redimensionada en el centro
            x_offset = (TARGET_WIDTH - new_width) // 2
            y_offset = (TARGET_HEIGHT - new_height) // 2
            
            # 7. Pegar la imagen redimensionada en el centro del lienzo
            canvas.paste(img, (x_offset, y_offset))
            
            # 8. Preparar el buffer de memoria para guardar la imagen final
            temp_buffer = BytesIO()
            
            # Determina el formato (JPEG o PNG) basado en la extensión original
            file_extension = os.path.splitext(self.image.name)[1].lower()
            img_format = 'PNG' if file_extension == '.png' else 'JPEG'

            # Guarda la imagen final (el lienzo) en el buffer
            canvas.save(temp_buffer, format=img_format, quality=90)
            
            # 9. Reemplaza la imagen antigua en el ImageField con la nueva data del lienzo
            self.image.file = ContentFile(temp_buffer.getvalue())
            
            # 10. Guarda el modelo *otra vez*, actualizando SOLO el campo 'image'
            super().save(update_fields=['image'])


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
            # Puedes ajustar el placeholder a 250x250 para que coincida con el tamaño redimensionado
            return 'https://via.placeholder.com/250x250.png?text=Sin+Imagen'

    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in=ids)

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
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
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-date')