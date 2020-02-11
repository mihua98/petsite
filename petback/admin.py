from django.contrib import admin
from .models import PetCategory, LostPet

# Register your models here.

class LostPetAdmin(admin.ModelAdmin):
    list_display = ['name',  'views', 'pet_type']
    fields = ['name', 'pet_img', 'intro', 'contact_way',  'pet_type', 'created_time']

admin.site.register(LostPet,LostPetAdmin)
admin.site.register(PetCategory)
