from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.db.models import Q
from markdown.extensions.toc import TocExtension
import markdown
from pure_pagination.mixins import PaginationMixin
import re

from petadopted.models import Petadopted, Category, Tag


# Create your views here.


class PetadoptedListView(PaginationMixin, ListView):
    """ 博客列表页 """
    model = Petadopted
    template_name = 'petadopted/petadoptedlist.html'
    context_object_name = 'petadopted_list'
    paginate_by = 10  # 分页


class PetadoptedDetailView(DetailView):
    """ 博客详情页 """
    model = Petadopted
    template_name = 'petadopted/petadopteddetails.html'
    context_object_name = 'petadopted'

    def get(self, request, *args, **kwargs):
        # get 方法返回的是一个 HttpResponse 实例
        response = super(PetadoptedDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()  # 阅读量+1
        return response

    def get_object(self, queryset=None):
        post = super().get_object(queryset=None)

        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ])
        post.body = md.convert(post.body)
        m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
        post.toc = m.group(1) if m is not None else ''
        return post


class ArchiveView(PetadoptedListView):
    """ 按时间筛选 """

    def get_queryset(self):
        return super(ArchiveView, self).get_queryset().filter(created_time__year=self.kwargs.get('year'),
                                                              created_time__month=self.kwargs.get('month'))


class CategoryView(PetadoptedListView):
    """ 按分类筛选 """

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


class TagView(PetadoptedListView):
    """ 按标签筛选 """

    def get_queryset(self):
        t = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=t)



class SearchView(PetadoptedListView):
    def get_queryset(self):
        q = self.request.GET.get('q')
        if not q:
            messages.add_message(self.request, messages.ERROR, '请输入搜索关键词', extra_tags='danger')
            return redirect('petadopted:list')

        petadopted_list = Petadopted.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
        return petadopted_list
