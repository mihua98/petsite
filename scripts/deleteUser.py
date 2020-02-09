import os
import sys
import django

# 将项目根目录添加到 Python 的模块搜索路径中
back = os.path.dirname
BASE_DIR = back(back(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "petsite.settings")
    django.setup()

    from users.models import MyUser

    print(MyUser.objects.all())
    MyUser.objects.filter(username='970911356@qq.com').delete()
    MyUser.objects.filter(username='3127644415@qq.com').delete()
    print(MyUser.objects.all())
