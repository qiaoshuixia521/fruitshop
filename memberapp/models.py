# coding=UTF-8
from django.db import models
# python2.x
from django.urls import reverse    #下文没有用到，也不知道是什么意思，所以先注释掉


# 商品类型


class GoodsType(models.Model):
    title = models.CharField('名称', max_length=30)
    desc = models.CharField('描述', max_length=200, default='商品描述')
    flag = models.IntegerField(default=0)
    picture = models.ImageField(upload_to='static/image/good_type', default='normal.png')
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta():
        db_table = 'goods_Type'


# 商品字段
class Goods(models.Model):
    title = models.CharField('名称', max_length=50)
    price = models.DecimalField('商品价格', max_digits=8, decimal_places=2)
    desc = models.CharField('描述', max_length=1000)
    # desc = models.CharField('描述', max_length=1000, default='商品的描述信息')
    picture = models.ImageField('商品照片', upload_to='static/images/goods',default='normal.png')
    isDelete = models.BooleanField(default=False)
    type = models.ForeignKey(GoodsType,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/detail/?good={}/'.format(self.id)

    class Meta():
        db_table = 'goods'


