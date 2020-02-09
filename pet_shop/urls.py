from django.urls import path

from pet_shop.views import *

app_name = 'pet_shop'
urlpatterns = [
    path('', ProductListView.as_view(), name='list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='detail'),
]
