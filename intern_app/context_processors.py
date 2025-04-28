from .models import CartItem, Categories , Billing,BilledItems, Products,Resimler
from django.shortcuts import get_object_or_404
from django.apps import apps
from django.contrib import admin
from django.shortcuts import render
from django.forms import modelform_factory
from collections import defaultdict

# Context Processors burada oluşturulan fonksiyonların şablonlarını her sayfaya kullanılabilir hale getirir.


def admin_links(request):
    """Tüm admin'e kayıtlı modelleri global context olarak döndürür"""
    models = []

    for model in apps.get_models():
        if admin.site.is_registered(model):
            app_label = model._meta.app_label
            model_name = model._meta.model_name
            verbose_name = model._meta.verbose_name_plural
         

            models.append({
                "app_label": app_label,
                "model_name": model_name,
                "verbose_name": verbose_name,
        
            })

    return {"admin_models": models}  # Global olarak admin_models kullanılabilir

def cart_items_processor(request):
    # Kullanıcının giriş yapdıysa
    if request.user.is_authenticated:
        # Kullanıcının sepetteki ürünlerini al
        cart_items = CartItem.objects.filter(user=request.user)
        # Sepetteki ürünlerin toplam fiyatını göster
        total_price = sum(item.cart_name.product_price *
                          item.cart_quantity for item in cart_items)
    # Ürün yoksa sepetteki ürünleri boş döndür ve toplam fiyatı 0 göster
    else:
        cart_items = []
        total_price = 0

    return {'cart_items': cart_items, 'total_price': total_price}


def categories_processor(request):
    categories_filtered = Categories.objects.filter(parent_categories=None).order_by('name')[:5]
    categories = Categories.get_main_categories()  # Kendi metodunla al
    return {'categories': categories,'categories_filtered':categories_filtered}  # Template'e gönder

# Alt kategorileri views.py fonksiyonunda sürekli kullanmak yerine genel kullanıma almak
def sub_categories_processor(request):
    # Url'de slug olup olmadığını kontrol eder. Slug varsa alır yoksa 404 hatası verir
    if 'slug' in request.resolver_match.kwargs:
        slug = request.resolver_match.kwargs.get('slug')
        category = get_object_or_404(Categories, slug=slug)
        # Alınan kategorilerin alt kategorisini alır
        sub_categories = category.sub_categories.all()
        return {'sub_categories': sub_categories}
    # Alt kategori yoksa boş döner.
    return {'sub_categories': []}

def BillingProcessor(request):
    billed_items = BilledItems()
    if request.user.is_authenticated:
        bills = Billing.objects.filter(user=request.user)
        billed_items = BilledItems.objects.filter(bills__user=request.user)
    else:
        bills = []
        billed_items = []
        only_product_image = []

    
    grouped_items = defaultdict(list)
    for item in billed_items:
        grouped_items[item.bills.id].append(item)

    return {
        "bills":bills,
        "billed_items":billed_items,
        "grouped_items":grouped_items,
      
    }
    
def gorseller(request):
    resimler = Resimler.objects.all()

    return {'resim':resimler}