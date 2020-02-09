from django import forms
from captcha.fields import CaptchaField

from users.models import MyUser


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True, error_messages={'invalid': '邮箱格式不正确'})
    password = forms.CharField(min_length=6, required=True, error_messages={'min_lenth': '密码长度小于6位'})
    captcha = CaptchaField(required=True, error_messages={'invalid': '验证码错误'})


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6)


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


class NewPwdForm(forms.Form):
    pwd1 = forms.CharField(required=True, min_length=6)
    pwd2 = forms.CharField(required=True, min_length=6)


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['nickname', 'gender']
