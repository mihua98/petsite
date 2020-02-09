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

from petblog.models import Post, Category, Tag
from petblog.forms import CommentForm


# Create your views here.


class PostListView(PaginationMixin, ListView):
    """ 博客列表页 """
    model = Post
    template_name = 'petblog/petblog-list.html'
    context_object_name = 'post_list'
    paginate_by = 10  # 分页


class PostDetailView(DetailView):
    """ 博客详情页 """
    model = Post
    template_name = 'petblog/petblog-details.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # get 方法返回的是一个 HttpResponse 实例
        response = super(PostDetailView, self).get(request, *args, **kwargs)
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


class ArchiveView(PostListView):
    """ 按时间筛选 """

    def get_queryset(self):
        return super(ArchiveView, self).get_queryset().filter(created_time__year=self.kwargs.get('year'),
                                                              created_time__month=self.kwargs.get('month'))


class CategoryView(PostListView):
    """ 按分类筛选 """

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


class TagView(PostListView):
    """ 按标签筛选 """

    def get_queryset(self):
        t = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=t)


@require_POST
def comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
    userid = request.user.id
    if not userid:
        messages.add_message(request, messages.ERROR, '您还未登录,请登录后进行评论!', extra_tags='danger')
        return redirect(post)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.user_id = userid
        comment.save()
        messages.add_message(request, messages.SUCCESS, '评论发表成功！', extra_tags='success')
        return redirect(post)

    context = {
        'post': post,
        'form': form,
    }
    messages.add_message(request, messages.ERROR, '评论发表失败！请修改评论中的错误后重新提交。', extra_tags='danger')
    return render(request, 'petblog/petblog-details.html', context=context)


class SearchView(PostListView):
    def get_queryset(self):
        q = self.request.GET.get('q')
        if not q:
            messages.add_message(self.request, messages.ERROR, '请输入搜索关键词', extra_tags='danger')
            return redirect('petblog:list')

        post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
        return post_list
