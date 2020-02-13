from django.urls import path

from . import views

app_name = 'petback'

urlpatterns = [

    path('', views.PetbackListView.as_view(), name='list'),
    path('<int:pk>/', views.PetbackDetailView.as_view(), name='detail'),
    path('categories/<int:pk>', views.PetCategoryView.as_view(), name='category'),
    path('search/', views.SearchView.as_view(), name='search'),
]
