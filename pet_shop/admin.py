from django.contrib import admin
from pet_shop.models import *


# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'num', 'sales', 'favorites', 'views', 'pro_type']
    fields = ['name', 'price', 'old_price', 'num', 'pro_type', 'main_img', 'intro',
              'details']


admin.site.register(Product, ProductAdmin)
admin.site.register(ProCategory)
admin.site.register(ProPic)
