# Generated by Django 3.0.1 on 2020-02-21 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_auto_20180304_1535'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goodscategorybrand',
            name='category',
        ),
        migrations.RemoveField(
            model_name='indexad',
            name='category',
        ),
        migrations.RemoveField(
            model_name='indexad',
            name='goods',
        ),
        migrations.AlterField(
            model_name='goods',
            name='goods_front_image',
            field=models.ImageField(blank=True, null=True, upload_to='product/main_img/', verbose_name='封面图'),
        ),
        migrations.AlterField(
            model_name='goodscategory',
            name='category_type',
            field=models.IntegerField(choices=[(1, '一级类目'), (2, '二级类目')], help_text='类目级别', verbose_name='类目级别'),
        ),
        migrations.DeleteModel(
            name='Banner',
        ),
        migrations.DeleteModel(
            name='GoodsCategoryBrand',
        ),
        migrations.DeleteModel(
            name='IndexAd',
        ),
    ]
