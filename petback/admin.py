from django.contrib import admin
from .models import *


# Register your models here.

class LostPetAdmin(admin.ModelAdmin):
    list_display = ['name', 'views', 'pet_type']
    fields = ['name', 'pet_img', 'intro', 'contact_way', 'pet_type']


    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)

admin.site.register(LostPet, LostPetAdmin)
admin.site.register(PetCategory)
