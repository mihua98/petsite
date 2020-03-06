from django.urls import reverse
from datetime import datetime
from django.db import models

# Create your models here.
from DjangoUeditor.models import UEditorField

# Create your models here.
# class ProCategory(models.Model):
#     name = models.CharField('类别名称', max_length=100)
#
#     class Meta:
#         verbose_name = '分类'
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.name


class GoodsCategory(models.Model):
    """
    商品多级分类
    """
    CATEGORY_TYPE = (
        (1, "一级类目"),
        (2, "二级类目"),
    )

    name = models.CharField(default="", max_length=30, verbose_name="类别名", help_text="类别名")
    code = models.CharField(default="", max_length=30, verbose_name="类别code", help_text="类别code")
    desc = models.TextField(default="", verbose_name="类别描述", help_text="类别描述")
    # 设置目录树的级别
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name="类目级别", help_text="类目级别")
    # 设置models有一个指向自己的外键
    parent_category = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True,
                                        verbose_name="父类目级别", help_text="父目录", related_name="sub_cat")
    is_tab = models.BooleanField(default=False, verbose_name="是否导航", help_text="是否导航")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "商品类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

#
# class Product(models.Model):
#     name = models.CharField('商品名称', max_length=30)
#     price = models.FloatField('单价')
#     old_price = models.FloatField('原单价', default=0)
#     num = models.PositiveIntegerField('数量')
#     sales = models.PositiveIntegerField('销量', default=0)
#     favorites = models.PositiveIntegerField('收藏数', default=0)
#     views = models.PositiveIntegerField('阅读量', default=0, editable=False)  # 正整数
#     pro_type = models.ForeignKey(ProCategory, verbose_name='分类', on_delete=models.CASCADE)
#     main_img = models.ImageField('商品主图', upload_to='product/main_img/%Y/%m',
#                                  default='product/product-4.jpg')
#     intro = models.CharField('简介', max_length=256, default='')
#     details = models.TextField('详情')
#     created_time = models.DateTimeField('添加时间', default=timezone.now)
#
#     class Meta:
#         verbose_name = '商品'
#         verbose_name_plural = verbose_name
#
#     def get_absolute_url(self):
#         return reverse('pet_shop:detail', kwargs={'pk': self.pk})
#
#     def increase_views(self):
#         self.views += 1
#         self.save(update_fields=['views'])  # 更新数据库中的views字段
#
#     def increase_sales(self):
#         self.sales += 1
#         self.save(update_fields=['sales'])
#
#     def increase_favorites(self):
#         self.favorites += 1
#         self.save(update_fields=['favorites'])
#
#     def __str__(self):
#         return self.name


class Goods(models.Model):
    """
    商品
    """
    category = models.ForeignKey(GoodsCategory, on_delete=models.CASCADE, verbose_name="商品类目")
    goods_sn = models.CharField(max_length=50, default="", verbose_name="商品唯一货号")
    name = models.CharField(max_length=100, verbose_name="商品名")
    click_num = models.IntegerField(default=0, verbose_name="点击数")
    sold_num = models.IntegerField(default=0, verbose_name="商品销售量")
    fav_num = models.IntegerField(default=0, verbose_name="收藏数")
    goods_num = models.IntegerField(default=0, verbose_name="库存数")
    market_price = models.FloatField(default=0, verbose_name="市场价格")
    shop_price = models.FloatField(default=0, verbose_name="本店价格")
    goods_brief = models.TextField(max_length=500, verbose_name="商品简短描述")
    goods_desc = UEditorField(verbose_name=u"内容", imagePath="product/main_img/%Y/%m/", width=1000, height=300,
                              filePath="product/files/%Y/%m/", default='')
    ship_free = models.BooleanField(default=True, verbose_name="是否承担运费")
    # 首页中展示的商品封面图
    goods_front_image = models.ImageField(upload_to="product/main_img/%Y/%m", null=True, blank=True,
                                          verbose_name="封面图", default='product/product-4.jpg')
    # 首页中新品展示
    is_new = models.BooleanField(default=False, verbose_name="是否新品")
    # 商品详情页的热卖商品，自行设置
    is_hot = models.BooleanField(default=False, verbose_name="是否热销")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '商品信息'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('pet_shop:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        self.click_num += 1
        self.save(update_fields=['click_num'])  # 更新数据库中的views字段

    def increase_sales(self):
        self.sold_num += 1
        self.save(update_fields=['sold_num'])

    def increase_favorites(self):
        self.fav_num += 1
        self.save(update_fields=['fav_num'])

    def __str__(self):
        return self.name


# class ProPic(models.Model):
#     product = models.ForeignKey(Product, verbose_name='商品', on_delete=models.CASCADE)
#     image = models.ImageField('商品图', upload_to='product/%Y/%m')
#     created_time = models.DateTimeField('添加时间', default=timezone.now)
#
#     class Meta:
#         verbose_name = '商品图片'
#         verbose_name_plural = verbose_name

class GoodsImage(models.Model):
    """
    商品轮播图
    """
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name="商品", related_name="images")
    image = models.ImageField(upload_to="", verbose_name="图片", null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '商品轮播'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class HotSearchWords(models.Model):
    """
    搜索栏下方热搜词
    """
    keywords = models.CharField(default="", max_length=20, verbose_name="热搜词")
    index = models.IntegerField(default=0, verbose_name="排序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '热搜排行'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.keywords
