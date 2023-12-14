from django.contrib import admin
from .models import *
# Register your models here.

class AdminProduct(admin.ModelAdmin):
    list_display = ['name','price','category']

class AdminCustomer(admin.ModelAdmin):
    list_display = ['first_name','last_name','email','phone']

class AdminOrder(admin.ModelAdmin):
    list_display=['product','customer','date']

admin.site.register(Product,AdminProduct)
admin.site.register(Category)
admin.site.register(Customer,AdminCustomer)
admin.site.register(Order,AdminOrder)