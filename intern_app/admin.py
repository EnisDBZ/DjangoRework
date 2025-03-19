from django.contrib import admin
from .models import PersonUser,Products,CartItem,Categories
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    filter_horizontal = ("sub_categories",) # Sona virgül eklemenin sebebi tamamen pythonın bunu tuple olarak algılaması için

admin.site.register(PersonUser)
admin.site.register(Products)
admin.site.register(CartItem)
admin.site.register(Categories, CategoryAdmin)
