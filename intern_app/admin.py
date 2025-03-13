from django.contrib import admin
from .models import PersonUser,Products,CartItem
# Register your models here.

admin.site.register(PersonUser)
admin.site.register(Products)
admin.site.register(CartItem)