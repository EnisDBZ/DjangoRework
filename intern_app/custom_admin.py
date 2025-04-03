from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import admin
from django.apps import apps
from django.urls import reverse
from django.forms import modelform_factory
from django.http import Http404
from django import forms
# Burada tüm custom-admin sayfasının fonksiyonları yer alacaktır.,
def model_silme(request,model_name,model_id ):
    tum_modeller = apps.get_model("intern_app",model_name)
    model_objects = tum_modeller.objects.get(id = model_id)

    model_objects.delete()

    return redirect(request.META.get('HTTP_REFERER'))
# Obje güncelleme fonksiyonu

def dynamic_model_item_update(request,app_label,model_name,object_id):
    
    try:
        model= apps.get_model(app_label,model_name)
    except LookupError:
        raise Http404("Böyle bir obje bulunmuyor.")
    
    # Model ve nesnesini alıyoruz.
    model_object = get_object_or_404(model,id=object_id)
    verbose_name = model._meta.verbose_name_plural

    #Formu oluşturuyoruz.
    modelForm = modelform_factory(model,fields="__all__")

   

    if request.method == 'POST':
        form = modelForm(request.POST,request.FILES,instance=model_object)
        if form.is_valid(): # Eğer form geçerliyse formu kaydet
            form.save()
            return redirect(reverse("intern_app:update_model",kwargs={"app_label":app_label,"model_name":model_name,"object_id":model_object.id}))
    else:
            form = modelForm(instance=model_object) 
        
    context = {
     "model_object":model_object,
     "model_name":model_name,
     "form":form,
     "verbose_name":verbose_name,
    }
    return render(request, "intern_app/custom_admin_update_item.html", context)

# Obje ekleme fonksiyonu
def dynamic_model_item_add(request,app_label, model_name):
  
    
    # Modeli getir
    try:
        model = apps.get_model(app_label, model_name)
    except LookupError:
        raise Http404("Böyle bir model bulunamadı.")

    # Model nesnelerini ve adını al
    model_objects = model.objects.all()
    verbose_name = model._meta.verbose_name_plural

    # Dinamik Model Formu oluştur
    ModelForm = modelform_factory(model, fields="__all__")

    if request.method == "POST":
        form = ModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse("intern_app:add_model", kwargs={"app_label": app_label, "model_name": model_name}))  
    else:
        form = ModelForm()

    context = {
        "model_objects": model_objects,
        "verbose_name": verbose_name,
        "form": form,
        "model_name": model_name
    }

    return render(request, "intern_app/custom_admin_add_item.html", context)

def admin_links(request):
    # Modelleri koymak için liste
    models = []
    # Uygulamamızdaki modelleri model isminde alıyoruz.
    for model in apps.get_models():
        # Admin'e kayıtlı olup olmadığını kontrol ediyoruz.
        if admin.site.is_registered(model):
            app_label = model._meta.app_label # Uygulama Adı
            model_name = model._meta.model_name # Model Adı
            verbose_name = model._meta.verbose_name_plural # Modelin çoğul adı
            # Aldığımız verileri listeye ekliyoruz.
            models.append({"app_label": app_label, "model_name": model_name,"verbose_name":verbose_name})

    return render(request,"intern_app/custom-admin.html", {"models": models})

def admin_links_pages(request, app_label, model_name):
    model_class = apps.get_model(app_label, model_name)
    model_objects = model_class.objects.all()
    verbose_name = model_class._meta.verbose_name_plural
    model_name = model_class._meta.model_name
    app_label = model_class._meta.app_label
    
    model_data = []
    for obj in model_objects:
        category_type = "Alt Kategori" if hasattr(obj, 'parent_categories') and obj.parent_categories.exists() else "Ana Kategori"

        model_data.append({
            "obj": obj,
            "category_type": category_type,
            
        })

    context = {
        "model_objects": model_objects,
        "model_class": model_class,
        "model_name":model_name,
        "model_data":model_data,
        "app_label":app_label,
        "verbose_name": verbose_name,
        "category_header":"Kategori Türü",
        
    }

    return render(request, 'intern_app/custom_admin_pages.html', context)