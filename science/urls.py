from django.urls import path
from . import views


app_name = 'science'
urlpatterns = [
    path('', views.ScienceListView.as_view(), name='list'),
    path('<int:pk>/', views.ScienceDetailView.as_view(), name='detail'),
    path('archive/<int:year>/<int:month>/', views.ArchiveView.as_view(), name='archive'),
    path('categories/<int:pk>', views.CategoryView.as_view(), name='category'),
    path('tags/<int:pk>', views.TagView.as_view(), name='tag'),
    path('search/', views.SearchView.as_view(), name='search'),
]