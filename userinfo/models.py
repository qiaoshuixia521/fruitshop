# coding=UTF-8
from django.db import models
from django import forms
# Create your models here.
# class Userinfo(forms.From):... 可以使用内置的表单验证渠道



# 用户信息
class UserInfo(models.Model):
    email = models.CharField('邮箱', max_length=40, db_column='uemail', null=False)
    uname = models.CharField('用户名', max_length=50, db_column='uname', null=False)
    upassword = models.CharField('密码', max_length=200, db_column='upassword', null=False)
    isban = models.BooleanField('禁用', default=False)
    # isactive = models.BooleanField('激活', default = False)
    # ucellphone = models.CharField('手机', default ='086')

    def __str__(self):
        return self.uname

    def get_absolute_url(self):
        return '???'

    class Meta():
        db_table = 'users'


#
class Address(models.Model):
    aname = models.CharField('姓名', max_length=30, db_column='aname', null=False)
    address = models.CharField('收站点', max_length=150, db_column='address', null=False)
    cellphone = models.CharField('手机号', max_length=15, db_column='cellphone', null=False)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)

    def __str__(self):
        return self.aname

    def get_absolute_url(self):
        return '???'

    class Meta():
        db_table = 'address'