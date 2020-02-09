from django.db import models
from django.contrib.auth.models import AbstractUser

from datetime import datetime


# Create your models here.
class MyUser(AbstractUser):
    """用户表"""
    nickname = models.CharField('昵称', max_length=20, default='')
    gender = models.CharField('性别', max_length=6, choices=(('male', '男'),
                                                           ('female', '女'),
                                                           ('secret', '保密'),
                                                           ), default='secret')
    address = models.CharField('地址', max_length=200, default='湖南省长沙市芙蓉区湖南农业大学')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.nickname if self.nickname != '' else self.username


class EmailVerifyRecord(models.Model):
    """
    邮箱验证码
    """
    code = models.CharField('验证码', max_length=80)
    email = models.EmailField('邮箱', max_length=50)
    send_type = models.CharField('验证码类型', choices=(('register', '注册'), ('find', '找回')), max_length=10,
                                 default='register')
    send_time = models.DateTimeField('发送时间', default=datetime.now)

    class Meta:
        verbose_name = '邮箱验证码信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.code}({self.email})'
