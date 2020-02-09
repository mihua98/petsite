from django.urls import path

from . import views

app_name = 'petblog'
urlpatterns = [
    path('', views.PostListView.as_view(), name='list'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    path('archive/<int:year>/<int:month>/', views.ArchiveView.as_view(), name='archive'),
    path('categories/<int:pk>', views.CategoryView.as_view(), name='category'),
    path('tags/<int:pk>', views.TagView.as_view(), name='tag'),
    path('comment/<int:pk>', views.comment, name='comment'),
    path('search/', views.SearchView.as_view(), name='search'),
]
