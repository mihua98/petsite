from django.contrib import admin
from .models import Science, Category, Tag
# Register your models here.


class ScienceAdmin(admin.ModelAdmin):
    list_display = ['title','created_time','category','author']
    fields = ['title','body','excerpt','category','tags','views','science_img']

admin.site.register(Science,ScienceAdmin)
admin.site.register(Category)
admin.site.register(Tag)
