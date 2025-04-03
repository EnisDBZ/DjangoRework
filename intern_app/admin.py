from django.contrib import admin
from .models import PersonUser, Products, CartItem, Categories
# Register your models here.

class PersonUserAdmin(admin.ModelAdmin):
    # Arama yapılacak alanları buraya ekleyin
    search_fields = ['username', 'email']


class CategoriesAdmin(admin.ModelAdmin):
    # Sona virgül eklemenin sebebi tamamen pythonın bunu tuple olarak algılaması için''
    filter_horizontal = ("sub_categories",)

    # Method to check if a category is a subcategory
    def is_subcategory(self, obj):
        return "Alt Kategori" if obj.parent_categories.exists() else "Ana Kategori"

    # Display the method result in the list view
    is_subcategory.short_description = "Kategori Türü"

    # Customize the list display to include the is_subcategory method
    list_display = ('name', 'is_subcategory', 'description', 'slug')


class ListedProducts(admin.ModelAdmin):
    list_display = ("product_name", "get_categories",
                    "product_description", "product_price")
    list_filter = ('product_category',)

    # Kategorileri virgülle ayırarak listelemek için bir metod

    def get_categories(self, obj):
        return ", ".join([category.name for category in obj.product_category.all()])

    # get_categories metodunun admin panelinde başlık olarak görünmesi
    get_categories.short_description = "Ürün Kategorisi"


# Register the Categories model with the custom admin class
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(PersonUser, PersonUserAdmin)
admin.site.register(Products, ListedProducts)
admin.site.register(CartItem)
