from django.db import models
from autoslug import AutoSlugField
from django.urls import reverse
from django.contrib.auth.models import AbstractUser,Permission
from django.core.validators import EmailValidator,MinLengthValidator, RegexValidator

# Create your models here.

# Kategori modeli
class Categories(models.Model):
    name = models.CharField(max_length=255,unique=True,verbose_name="Kategori İsmi")
    description = models.CharField(max_length=255,null=True,verbose_name="Kategori Açıklaması")
    image = models.ImageField(upload_to='category_images/',verbose_name="Kategori Görseli")
    slug = AutoSlugField(populate_from="name",unique=True,verbose_name="Alan Adı")
    sub_categories = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="parent_categories",verbose_name="Alt Kategori olmasını istediğiniz kategorileri seçin:",
                                            help_text="Birden fazla kategori seçmek için CTRL tuşuna basılı tutunuz." \
                                            "\n Aynı zamanda seçimi iptal etmek için CTRL tuşuna basılı tutup seçimi iptal edilmek istenen kategoriye tıklayın. ")
   
    # Modelin tüm objelerini almak için basitleştirilmiş fonksiyon
    @staticmethod
    def get_all_categories():
        return Categories.objects.all()
    # Modelin sadece ana kategorilerini almak için oluşturulan fonksiyon
    @staticmethod
    def get_main_categories():
        # Başka bir kategorinin alt kategorisi OLMAYAN ana kategorileri getir
        return Categories.objects.filter(parent_categories__isnull=True)
    
    def get_absolute_url(self):
        return reverse('intern_app:subcategory_products',kwargs={"slug":self.slug})
    def get_absolute_url_cat(self):
        return reverse('intern_app:category_products',kwargs={"slug":self.slug})
  

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


# Authentication Modeli
class PersonUser(AbstractUser):
    email = models.EmailField(validators=[EmailValidator()],unique = True)
    password = models.CharField(validators=[MinLengthValidator(8)],max_length=16)

    def __str__(self):
        return self.username
 
    
    class Meta():
        verbose_name ="Kullanıcı"
        verbose_name_plural = "Kullanıcılar"

# Ürün modeli
class Products(models.Model):
    product_name = models.CharField(max_length=255, verbose_name="Ürün Adı")
    product_category = models.ManyToManyField(Categories,related_name="products",verbose_name="Ürün Kategorisi",help_text="Birden fazla kategori seçmek için CTRL tuşuna basılı tutunuz. \n Aynı zamanda seçimi iptal etmek için CTRL tuşuna basılı tutup seçimi iptal edilmek istenen kategoriye tıklayın.")
    
    #product_category = models.ForeignKey(Categories, on_delete=models.CASCADE,related_name='products' ,null=True)
    product_description = models.TextField(null=True,verbose_name="Ürün Açıklaması")
    product_price = models.DecimalField(max_digits=9,decimal_places=2,verbose_name="Ürün Fiyatı")    
    product_image = models.ImageField(upload_to='products/',verbose_name="Ürün Görseli")   
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.product_name
    


    
    class Meta:
        # Admin panelinde nasıl gözükeceği
        verbose_name= 'Ürün'
        verbose_name_plural = 'Ürünler'
        
# Sepetteki ürünler modeli
class CartItem(models.Model):
    cart_name = models.ForeignKey(Products,on_delete=models.CASCADE,verbose_name="Ürün Adı")
    cart_quantity = models.PositiveIntegerField(default=0,verbose_name="Ürün Sayısı")
    user = models.ForeignKey(PersonUser,on_delete=models.CASCADE,verbose_name="Kullanıcı")

    def __str__(self):
        return f"{self.cart_quantity} x {self.cart_name.product_name}"
    
    # Tekil ürünün toplam fiyatını görmek için adet x fiyat
    def cart_total(self):
        return self.cart_quantity * self.cart_name.product_price
     
    class Meta:
        verbose_name = "Sepete Ürün"
        verbose_name_plural = "Sepet"

class CartItemQuickBuy(models.Model):
    user = models.ForeignKey(PersonUser,on_delete = models.CASCADE,verbose_name="Kullanıcı")
    item_name = models.ForeignKey(Products, on_delete=models.CASCADE,verbose_name="Ürün Adı")
    item_quantity = models.PositiveIntegerField(default=0,verbose_name="Ürün Sayısı")

    def __str__(self):
        return f"{self.item_quantity} x {self.item_name.product_name}"
    
    # Tekil ürünün toplam fiyatını görmek için adet x fiyat

    def item_total(self):
        return self.item_quantity * self.item_name.product_price
    
 
class Billing(models.Model):
    user = models.ForeignKey(PersonUser,on_delete=models.CASCADE,verbose_name="Kullanıcı")
    name = models.CharField(max_length=255,null=False,verbose_name="İsim")
    surname = models.CharField(max_length=255,null=False,verbose_name="Soyisim")
    email = models.EmailField(validators=[EmailValidator()],null=False,verbose_name="E-Posta")
    telno = models.CharField(max_length=11,null=False,verbose_name="Telefon Numarası")
    city = models.CharField(max_length=255,null=False,verbose_name="İl")
    town = models.CharField(max_length=255,null=False,verbose_name="İlçe")
    zipcode = models.CharField(max_length=5,null=False,verbose_name="Zip Kodu")
    address = models.CharField(max_length=300,null=False,verbose_name="Adres")
    pay_method = models.CharField(max_length=255,null=False,verbose_name="Ödeme Yöntemi")
    card_no = models.CharField(max_length=16,null=False,verbose_name="Kart Numarası")
    card_exp = models.CharField(max_length=5,null=False,verbose_name="Kart Son Kullanma Tarihi")
    card_owner = models.CharField(max_length=255,null=False,verbose_name="Kart Sahibi İsim-Soyisim")
    card_cvv = models.CharField(max_length=3,null=False,verbose_name="Kart CVV")
    billing_total_price = models.DecimalField(max_digits=9,decimal_places=2,null=False, default=0,verbose_name="Toplam Fiyat")
    order_statuses = (
        ('Bekliyor','Bekliyor'),
        ('Yola Çıktı','Yola Çıktı'),
        ('Tamamlandı','Tamamlandı'),
    )
    status = models.CharField(max_length=150,choices=order_statuses,default='Bekliyor',verbose_name="Durum")
    message = models.TextField(null=True,verbose_name="")
    tracking_no = models.CharField(max_length=150,null=True,verbose_name="Takip No")
    create_date = models.DateTimeField(auto_now_add=True,verbose_name="Oluşturma Zamanı")
    update_date = models.DateTimeField(auto_now=True,verbose_name="Güncelleme Zamanı")
    
    class Meta:
        verbose_name = "Fatura"
        verbose_name_plural = "Faturalar"
    def __str__(self):
        return '{} - {}'.format(self.id,self.tracking_no)

class BilledItems(models.Model):
    bills = models.ForeignKey(Billing,on_delete=models.CASCADE, verbose_name = "Ürünün Ait Olduğu Fatura")
    product = models.ForeignKey(Products,on_delete=models.CASCADE,verbose_name="Ürün")
    no = models.CharField(max_length=150,null=True,verbose_name="Ürün Numarası")
    price = models.DecimalField(max_digits=9,decimal_places=2,null=False,verbose_name="Fiyat")
    quantity = models.IntegerField(null=False,verbose_name="Adet")

    class Meta:
        verbose_name = "Faturalanmış Ürün"
        verbose_name_plural = "Faturalanmış Ürünler"

    def __str__(self):
        return '{} - {}'.format(self.bills.id, self.no)
    
    def item_total_price(self):
        return self.price * self.quantity
    
class Resimler(models.Model):
    resim_isim = models.CharField(max_length=255,verbose_name="Resim Adı")
    resim_gorseli = models.ImageField(upload_to='reklam_gorsel/',verbose_name="Görsel")

    class Meta():
        verbose_name = "Resim"
        verbose_name_plural = "Resimler"
    def __str__(self):
        return self.resim_isim
    
class Address(models.Model):
    user = models.ForeignKey(PersonUser,on_delete=models.CASCADE,related_name='adres_user')
    address_title = models.CharField(max_length=255,default="Varsayılan Adres")
    name = models.CharField(max_length=255,null=False,verbose_name="İsim")
    surname = models.CharField(max_length=255,null=False,verbose_name="Soyisim")
    email = models.EmailField(validators=[EmailValidator()],null=False,verbose_name="E-Posta")
    telno = models.CharField(validators=[RegexValidator(regex=r'^\d{11}$')],max_length=11,null=False,verbose_name="Telefon Numarası")
    city = models.CharField(max_length=255,null=False,verbose_name="İl")
    town = models.CharField(max_length=255,null=False,verbose_name="İlçe")
    zipcode = models.CharField(validators=[RegexValidator(regex=r'\d{5}$')],max_length=5,null=False,verbose_name="Zip Kodu")
    open_address = models.CharField(max_length=300,null=False,verbose_name="Açık Adres")
    isDefault = models.BooleanField(default=False)

    def __str__(self):
        return self.address_title
    
class CreditCard(models.Model):
    user = models.ForeignKey(PersonUser,on_delete=models.CASCADE, related_name="credit_card")
    card_title = models.CharField(max_length=255,default="Varsayılan Kart")
    card_no = models.CharField(validators=[RegexValidator(regex=r'^\d{16}$',message="Kart numarasi 16 haneli olmalıdır!")],max_length=16,null=False,error_messages={"min_length":"Minimum 16 hane girmeniz gerekli"},verbose_name="Kart Numarası")
    card_exp = models.CharField(max_length=5,null=False,verbose_name="Kart Son Kullanma Tarihi")
    card_owner = models.CharField(validators=[RegexValidator(regex = r'^([a-zA-ZçÇğĞıİöÖşŞüÜ]{2,70} ?){2,4}$',message="İsim ve soyisminiz 2 ila 70 karakter arasında olmalı.")],error_messages={"min_length":"İsim ve soyisminiz toplamda 4 haneden az olmamalıdır!"},max_length=255,null=False,verbose_name="Kart Sahibi İsim-Soyisim")
    card_cvv = models.CharField(validators=[RegexValidator(regex=r'^\d{3}$',message="CVV 3 haneli olmalıdır!")],error_messages={"min_length":"CVV Minimum 3 haneli olmalıdır"},max_length=3,null=False,verbose_name="Kart CVV")
    isDefault = models.BooleanField(default=False)

    def __str__(self):
        return self.card_title 
    
    def last_four(self):
        return "**** **** **** " + self.card_no[-4:]