from django.shortcuts import render
from django.views.generic import ListView, DetailView

from pure_pagination.mixins import PaginationMixin

from pet_shop.models import *


# Create your views here.


class ProductListView(PaginationMixin, ListView):
    model = Product
    template_name = 'pet_shop/product-list.html'
    context_object_name = 'product_list'
    ordering = '-created_time'
    paginate_by = 12


class ProductDetailView(DetailView):
    model = Product
    template_name = 'pet_shop/product-details.html'
    context_object_name = 'product'

    def get(self, request, *args, **kwargs):
        # get 方法返回的是一个 HttpResponse 实例
        response = super(ProductDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()  # 阅读量+1
        return response
