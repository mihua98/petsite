from django.db import models
from django.utils import timezone
from django.urls import reverse
import markdown
from users.models import MyUser
from django.utils.html import strip_tags


# Create your models here.

class Category(models.Model):
    name = models.CharField('类别名称', max_length=100)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField('标签名称', max_length=100)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Science(models.Model):
    title = models.CharField('标题', max_length=70)
    body = models.TextField('正文')
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    modified_time = models.DateTimeField('修改时间')
    excerpt = models.CharField('摘要', max_length=200, blank=True)
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)
    author = models.ForeignKey(MyUser, verbose_name='作者', on_delete=models.CASCADE)
    views = models.PositiveIntegerField('阅读量', default=0, editable=False)  # 正整数
    science_img = models.ImageField('科普图片', upload_to='science/science_img/%Y/%m',
                                    default='science/product-9.jpg')

    class Meta:
        verbose_name = '科普'  # 指定对应的 model 在 admin 后台的显示名称
        verbose_name_plural = verbose_name  # 表示复数，中文没有复数表现形式,所以和上面一样
        ordering = ['-created_time']

    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        self.excerpt = strip_tags(md.convert(self.body))[:54]
        super().save(*args, **kwargs)

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])  # 更新数据库中的views字段

    def get_absolute_url(self):
        return reverse('science:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title
