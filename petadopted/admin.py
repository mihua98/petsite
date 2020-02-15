from django.contrib import admin
from .models import Petadopted, Category, Tag
# Register your models here.


class PetadoptedAdmin(admin.ModelAdmin):
    list_display = ['title','created_time','category','author']
    fields = ['title','body','excerpt','category','tags','pet_img']

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Petadopted,PetadoptedAdmin)
admin.site.register(Category)
admin.site.register(Tag)
