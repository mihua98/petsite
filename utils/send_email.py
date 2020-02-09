from random import Random
from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from petsite.settings import EMAIL_FROM
from petsite.settings import DOMAIN_NAME


def random_str(randomlength=10):
    ranstr = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        ranstr += chars[random.randint(0, length)]
    return ranstr


def send_register_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    ran_str = random_str(20)
    email_record.email = email
    email_record.code = ran_str
    email_record.send_type = send_type
    email_record.save()

    if send_type == 'register':
        email_title = 'PlusSeven宠物网 注册激活'
        email_body = '你好!\n' \
                     '感谢你注册PlusSeven宠物网。 \n' \
                     f'你的登录邮箱为：{email}。\n' \
                     '请点击下面的链接激活你的账号: \n' \
                     + DOMAIN_NAME + f'user/active/{ran_str}'
        send_mail(email_title, email_body, EMAIL_FROM, [email])

    elif send_type == 'find':
        email_title = 'PlusSeven宠物网 找回密码'
        email_body = '你好!\n' \
                     f'你找回密码的邮箱为：{email}。\n' \
                     '请点击下面的链接找回你的密码: \n' \
                     + DOMAIN_NAME + f'user/find/{ran_str}'
        send_mail(email_title, email_body, EMAIL_FROM, [email])
