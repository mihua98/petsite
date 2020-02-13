from django.contrib import admin
from .models import *


# Register your models here.

class LostPetAdmin(admin.ModelAdmin):
    list_display = ['name', 'views', 'pet_type']
    fields = ['name', 'pet_img', 'intro', 'contact_way', 'pet_type']


admin.site.register(LostPet, LostPetAdmin)
admin.site.register(PetCategory)
