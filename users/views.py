from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url

from users.forms import *
from users.models import *
from petblog.models import *
from pet_shop.models import *
from utils.send_email import send_register_email


# Create your views here.

class IndexView(View):
    """首页"""

    def get(self, request):
        post_list = Post.objects.all()[:3]  # 宠物博客
        product_list = Goods.objects.all()[:8]  # 宠物商品

        return render(request, 'users/index.html', context={
            'post_list': post_list,
            'product_list': product_list
        })


class RegisterView(View):
    """注册"""

    def get(self, request):
        register_form = RegisterForm()
        hashkey = CaptchaStore.generate_key()
        image_url = captcha_image_url(hashkey)
        return render(request, 'users/register.html', {
            'register_form': register_form,
            'hashkey': hashkey,
            'image_url': image_url,
        })

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', '')

            if MyUser.objects.filter(email=user_name):
                return render(request, 'users/register.html',
                              {'register_form': register_form,
                               'msg': '用户已经存在'
                               })

            password = request.POST.get('password', '')
            user = MyUser()
            user.username = user_name
            user.email = user_name
            user.is_active = False
            user.password = make_password(password)
            user.save()

            send_register_email(user_name)

            messages.add_message(request, messages.SUCCESS, '注册成功!请在邮箱中点击激活链接激活账号！')
            return render(request, 'users/register.html', {})
        else:
            hashkey = CaptchaStore.generate_key()
            image_url = captcha_image_url(hashkey)
            return render(request, 'users/register.html', {
                'register_form': register_form,
                'hashkey': hashkey,
                'image_url': image_url})


class ActiveView(View):
    """
    激活
    """

    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(send_type='register', code=active_code)
        if all_records:
            record = all_records[0]
            email = record.email
            user = MyUser.objects.get(email=email)
            user.is_active = True
            user.save()
            messages.add_message(request, messages.SUCCESS, '激活成功!')
            return render(request, 'users/login.html', {})
        else:
            messages.add_message(request, messages.ERROR, '激活失败!')
            return render(request, 'users/login.html')


class LoginView(View):
    """登陆"""

    def get(self, request):
        return render(request, 'users/login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            is_keep = request.POST.get('is_keep', '')
            user = authenticate(username=username, password=password)
            # 如果用户存在
            if user is not None and user.is_active:
                login(request, user)
                # 如果保持登陆状态
                if not is_keep:
                    # 关闭浏览器session实效
                    request.session.set_expiry(0)
                return HttpResponseRedirect(reverse('index'))
            else:
                return render(request, 'users/login.html', {'msg': '用户名或密码错误！'})
        else:
            return render(request, 'users/login.html', {'login_form': login_form})


class LogoutView(View):
    """
    退出
    """

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class ForgetPwdView(View):
    """忘记密码"""

    def get(self, request):
        forget_from = ForgetForm()
        hashkey = CaptchaStore.generate_key()
        image_url = captcha_image_url(hashkey)
        return render(request, 'users/forget_pwd.html', {
            'forget_form': forget_from,
            'hashkey': hashkey,
            'image_url': image_url,
        })

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        hashkey = CaptchaStore.generate_key()
        image_url = captcha_image_url(hashkey)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            send_register_email(email, 'find')
            messages.add_message(request, messages.SUCCESS, '邮件发送成功！请点击邮件中的链接找回密码')
            return render(request, 'users/forget_pwd.html', {
                'hashkey': hashkey,
                'image_url': image_url,
            })
        else:
            return render(request, 'users/forget_pwd.html', {
                'forget_form': forget_form,
                'hashkey': hashkey,
                'image_url': image_url,
            })


class ResetView(View):
    """找回密码页面"""

    def get(self, request, find_code):
        all_records = EmailVerifyRecord.objects.filter(send_type='find', code=find_code)
        if all_records:
            record = all_records[0]
            email = record.email
            messages.add_message(request, messages.SUCCESS, '请输入新密码')
            return render(request, 'users/new_pwd.html', {
                'email': email,
            })


class NewPwdView(View):
    """修改密码"""

    def post(self, request):
        newpwd_form = NewPwdForm(request.POST)
        if newpwd_form.is_valid():
            pwd1 = request.POST.get('pwd1', '')
            pwd2 = request.POST.get('pwd2', '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                messages.add_message(request, messages.ERROR, '两次输入的密码不一致')
                return render(request, 'users/new_pwd.html', {
                    'email': email
                })
            user = MyUser.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            messages.add_message(request, messages.SUCCESS, '密码修改成功!')
            return HttpResponseRedirect(reverse('users:login'))
        else:
            email = request.POST.get('email', '')
            messages.add_message(request, messages.ERROR, '您的输入有误,请重新输入')
            return render(request, 'users/new_pwd.html', {
                'email': email,
                'newpwd_form': newpwd_form,
            })


class UserInfoView(View):
    def get(self, request):
        return render(request, 'users/my-account.html', {})


class UpdateUserInfoView(View):
    """修改用户信息"""

    def post(self, request):
        info_form = UserInfoForm(request.POST, instance=request.user)
        if info_form.is_valid():
            info_form.save()
        return HttpResponseRedirect(reverse('users:userinfo'))


class UpdateUserPwdView(View):
    def post(self, request):
        pwd_form = NewPwdForm(request.POST)
        if pwd_form.is_valid():
            pwd1 = request.POST.get('pwd1', '')
            pwd2 = request.POST.get('pwd2', '')
            if pwd1 != pwd2:
                messages.add_message(request, messages.ERROR, '两次输入的密码不一致')
                return render(request, 'users/my-account.html')
            user = MyUser.objects.get(email=request.user.email)
            user.password = make_password(pwd2)
            user.save()
            messages.add_message(request, messages.SUCCESS, '密码修改成功!请重新登录')
        else:
            messages.add_message(request, messages.ERROR, '您的输入有误,请重新输入')
            return render(request, 'users/my-account.html')
        return HttpResponseRedirect(reverse('users:login'))
