from django.urls import path

from users.views import *

app_name = 'users'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  # 注册
    path('active/<slug:active_code>', ActiveView.as_view(), name='active'),  # 激活
    path('login/', LoginView.as_view(), name='login'),  # 登陆
    path('logout/', LogoutView.as_view(), name='logout'),  # 登出
    path('forget_pwd/', ForgetPwdView.as_view(), name='forget_pwd'),  # 忘记密码
    path('find/<slug:find_code>', ResetView.as_view(), name='find'),  # 从邮箱点击到找回密码页面
    path('new_pwd/', NewPwdView.as_view(), name='new_pwd'),  # 修改密码
    path('userinfo/', UserInfoView.as_view(), name='userinfo'),  # 个人中心
    path('userinfo/update', UpdateUserInfoView.as_view(), name='update_userinfo'),  # 修改个人信息
    path('userinfo/update_pwd', UpdateUserPwdView.as_view(), name='update_user_pwd'),  # 修改个人信息
]
