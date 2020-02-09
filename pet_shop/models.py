from django.db import models
from django.utils import timezone
from django.urls import reverse


# Create your models here.
class ProCategory(models.Model):
    name = models.CharField('类别名称', max_length=100)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField('商品名称', max_length=30)
    price = models.FloatField('单价')
    old_price = models.FloatField('原单价', default=0)
    num = models.PositiveIntegerField('数量')
    sales = models.PositiveIntegerField('销量', default=0)
    favorites = models.PositiveIntegerField('收藏数', default=0)
    views = models.PositiveIntegerField('阅读量', default=0, editable=False)  # 正整数
    pro_type = models.ForeignKey(ProCategory, verbose_name='分类', on_delete=models.CASCADE)
    main_img = models.ImageField('商品主图', upload_to='product/main_img/%Y/%m',
                                 default='product/product-4.jpg')
    intro = models.CharField('简介', max_length=256, default='')
    details = models.TextField('详情')
    created_time = models.DateTimeField('添加时间', default=timezone.now)

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('pet_shop:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])  # 更新数据库中的views字段

    def increase_sales(self):
        self.sales += 1
        self.save(update_fields=['sales'])

    def increase_favorites(self):
        self.favorites += 1
        self.save(update_fields=['favorites'])

    def __str__(self):
        return self.name


class ProPic(models.Model):
    product = models.ForeignKey(Product, verbose_name='商品', on_delete=models.CASCADE)
    image = models.ImageField('商品图', upload_to='product/%Y/%m')
    created_time = models.DateTimeField('添加时间', default=timezone.now)

    class Meta:
        verbose_name = '商品图片'
        verbose_name_plural = verbose_name
