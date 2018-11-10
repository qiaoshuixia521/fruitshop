#-*- coding: UTF-8 -*-r
from django.contrib import admin
from .models import *
# Register your models here.
import sys

# reload(sys)
# sys.setdefaultencoding("utf8")
admin.site.register(Goods)
admin.site.register(GoodsType)