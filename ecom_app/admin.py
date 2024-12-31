from django.contrib import admin
from .models import Product,Category,Order,Cart
# Register your models here.

class AdminProduct(admin.ModelAdmin):
    list_display=['name','price','category']

admin.site.register(Product,AdminProduct)


class AdminCategory(admin.ModelAdmin):
    list_display=['name']
admin.site.register(Category,AdminCategory)


class AdminOrder(admin.ModelAdmin):
    list_display=['order']
admin.site.register(Order)

class AdminCart(admin.ModelAdmin):
    list_display=['user','product','quantity']
admin.site.register(Cart,AdminCart)