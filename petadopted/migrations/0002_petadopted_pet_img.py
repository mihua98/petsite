# Generated by Django 3.0.1 on 2020-02-15 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petadopted', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='petadopted',
            name='pet_img',
            field=models.ImageField(default='petadopted/product-9.jpg', upload_to='petadopted/petadopted_img/%Y/%m', verbose_name='宠物图片'),
        ),
    ]
