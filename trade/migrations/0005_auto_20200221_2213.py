# Generated by Django 3.0.1 on 2020-02-21 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0004_auto_20190619_1650'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderinfo',
            name='signer_name',
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='pay_type',
            field=models.CharField(choices=[('alipay', '支付宝')], default='alipay', max_length=10, verbose_name='支付类型'),
        ),
    ]
