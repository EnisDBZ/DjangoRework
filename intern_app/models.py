from django.db import models
from django.contrib.auth.models import AbstractUser,Permission
from django.core.validators import EmailValidator,MinLengthValidator

# Create your models here.
class Categories(models.Model):
    name = models.CharField(max_length=255,unique=True,verbose_name="Kategori İsmi")
    description = models.CharField(max_length=255,null=True,verbose_name="Kategori Açıklaması")
    image = models.ImageField(upload_to='category_images/',verbose_name="Kategori Görseli")
    slug = models.SlugField(unique=True,verbose_name="Alan Adı")
    sub_categories = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="parent_categories",verbose_name="Alt Kategoriler")
    is_sub_cat = models.BooleanField(default=False,verbose_name="Alt Kategori mi?")
    # Modelin tüm objelerini almak için basitleştirilmiş fonksiyon
    @staticmethod
    def get_all_categories():
        return Categories.objects.all()
    # Modelin sadece ana kategorilerini almak için oluşturulan fonksiyon
    @staticmethod
    def get_main_categories():
        # Başka bir kategorinin alt kategorisi OLMAYAN ana kategorileri getir
        return Categories.objects.filter(parent_categories__isnull=True)
  

    def is_sub(self):
        # Eğer kategoriye ait alt kategori varsa, bu kategori bir alt kategoridir
        return self.parent_categories.exists()

    def __str__(self):
        # Kategori bir alt kategori ise, "Kategori Adı » AltKategori" formatında döner
        if self.is_sub():  # Kategori alt kategori ise
            parent_category_name = "Alt Kategori" if self.parent_categories.exists() else "Ana Kategori"
            return f"{self.name} » {parent_category_name}"
        
        # Eğer ana kategori ise, "Kategori Adı » AnaKategori" formatında döner
        return f"{self.name} » Ana Kategori"
    class Meta():
        verbose_name = 'Kategori'
        verbose_name_plural = 'Kategoriler'

class PersonUser(AbstractUser):
    email = models.EmailField(validators=[EmailValidator()],unique = True)
    password = models.CharField(validators=[MinLengthValidator(8)],max_length=16)

    def __str__(self):
        return self.username
    
    class Meta():
        verbose_name ="Kullanıcı"
        verbose_name_plural = "Kullanıcılar"

    
class Products(models.Model):
    product_name = models.CharField(max_length=255, verbose_name="Ürün Adı")
    product_category = models.ManyToManyField(Categories,related_name="products",verbose_name="Ürün Kategorisi")
    #product_category = models.ForeignKey(Categories, on_delete=models.CASCADE,related_name='products' ,null=True)
    product_description = models.TextField(null=True,verbose_name="Ürün Açıklaması")
    product_price = models.DecimalField(max_digits=9,decimal_places=2,verbose_name="Ürün Fiyatı")    
    product_image = models.ImageField(upload_to='products/',verbose_name="Ürün Görseli")   

    def __str__(self):
        return self.product_name
    class Meta:
        # Admin panelinde nasıl gözükeceği
        verbose_name= 'Ürün'
        verbose_name_plural = 'Ürünler'
        
class CartItem(models.Model):
    cart_name = models.ForeignKey(Products,on_delete=models.CASCADE,verbose_name="Ürün Adı")
    cart_quantity = models.PositiveIntegerField(default=0,verbose_name="Ürün Sayısı")
    user = models.ForeignKey(PersonUser,on_delete=models.CASCADE,verbose_name="Kullanıcı")

    def __str__(self):
        return f"{self.cart_quantity} x {self.cart_name.product_name}"
    
    def cart_total(self):
        return self.cart_quantity * self.cart_name.product_price
    class Meta:
        verbose_name = "Sepete Ürün"
        verbose_name_plural = "Sepet"