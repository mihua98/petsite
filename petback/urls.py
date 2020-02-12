from django.urls import path

from . import views

app_name = 'petback'

urlpatterns = [

    path('', views.petbacklist, name='list'),
    path('<int:pk>/', views.petbackDetail, name='detail'),
]
