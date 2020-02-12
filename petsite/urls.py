"""petsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users.views import IndexView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', IndexView.as_view(), name='index'),  # 首页
                  path('posts/', include('petblog.urls')),  # 宠物博客
                  path('products/', include('pet_shop.urls')),  # 宠物博客
                  path('user/', include('users.urls')),  # 用户管理
                  path('captcha', include('captcha.urls')),  # 验证码
                  path('petback/', include('petback.urls')),  # 宠物找回
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
