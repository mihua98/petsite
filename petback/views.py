from django.db.models import Q

from petback.models import *
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from pure_pagination.mixins import PaginationMixin
from django.contrib import messages
# Create your views here.


class PetbackListView(PaginationMixin,ListView):
    model = LostPet
    template_name = 'petback/petbacklist.html'
    context_object_name = 'lost_pet_list'
    paginate_by = 2

class PetbackDetailView(DetailView):
    model = LostPet
    template_name = 'petback/petback-details.html'
    context_object_name = 'lost_pet'

    def get(self,request,*args,**kwargs):
        response = super(PetbackDetailView,self).get(request,*args,**kwargs)
        self.object.increase_views()
        return response

class PetCategoryView(PetbackListView):
    # model = LostPet
    # template_name = '_categories.html'
    # context_object_name = 'category_list'
    def get_queryset(self):
        cate = get_object_or_404(PetCategory,pk=self.kwargs.get('pk'))
        return super(PetCategoryView,self).get_queryset().filter(pet_type=cate)



class SearchView(PetbackListView):
    def get_queryset(self):
        q = self.request.GET.get('q')
        if not q:
            messages.add_message(self.request, messages.ERROR, '请输入搜索关键词', extra_tags='danger')
            return redirect('petback:list')
        lost_pet = LostPet.objects.filter(Q(name__icontains=q) | Q(intro__icontains=q))
        return lost_pet


