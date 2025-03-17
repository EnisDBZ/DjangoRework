from django.db import models
from django.contrib.auth.models import AbstractUser,Permission
from django.core.validators import EmailValidator,MinLengthValidator

# Create your models here.
class Categories(models.Model):
    name = models.CharField(max_length=255,unique=True)
    image = models.ImageField(upload_to='category_images/')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    
    def Meta():
        verbose_name = 'Kategori'
        verbose_name_plural = 'Kategoriler'

class PersonUser(AbstractUser):
    email = models.EmailField(validators=[EmailValidator()],unique = True)
    password = models.CharField(validators=[MinLengthValidator(8)],max_length=16)

    def __str__(self):
        return self.username
    
class Products(models.Model):
    product_name = models.CharField(max_length=255)
    product_category = models.ForeignKey(Categories, on_delete=models.CASCADE,related_name='products' ,null=True)
    product_description = models.TextField(null=True)
    product_price = models.DecimalField(max_digits=9,decimal_places=2)    
    product_image = models.ImageField(upload_to='products/')   

    def __str__(self):
        return self.product_name
    class Meta:
        # Admin panelinde nasıl gözükeceği
        verbose_name= 'Ürün'
        verbose_name_plural = 'Ürünler'
        
class CartItem(models.Model):
    cart_name = models.ForeignKey(Products,on_delete=models.CASCADE)
    cart_quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(PersonUser,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.cart_quantity} x {self.cart_name.product_name}"
    
    def cart_total(self):
        return self.cart_quantity * self.cart_name.product_price
