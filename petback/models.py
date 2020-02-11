from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class PetCategory(models.Model):
    name = models.CharField('宠物类型', max_length=30)

    class Meta:
        verbose_name = '宠物类型'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class LostPet(models.Model):
    name = models.CharField('宠物姓名',max_length=20)
    pet_img = models.ImageField('宠物图片', upload_to='pet_back/pet_img/%Y/%m',
                                 default='pet_back/product-4.jpg')
    intro = models.CharField('简介', max_length=256, default='')
    contact_way = models.CharField('联系方式', max_length=256, default='')
    views = models.PositiveIntegerField('阅读量', default=0, editable=False)  # PositiveIntegerField:正整数
    pet_type = models.ForeignKey(PetCategory, verbose_name='宠物分类', on_delete=models.CASCADE)
    created_time = models.DateTimeField('添加时间', default=timezone.now)

    class Meta:
        verbose_name = '遗失宠物'
        verbose_name_plural = verbose_name

    def get_absolute_url(self): # 获得详情页的url
        return reverse('petback:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])  # 更新数据库中的views字段

    def __str__(self):
        return self.name