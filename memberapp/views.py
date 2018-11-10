#-*- coding: UTF-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.http import request, response
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.exceptions import ObjectDoesNotExist
from django.db import DataError, DatabaseError
import logging
import random
from django.http import JsonResponse
import math
from .models import *
from cartinfo.models import CartInfo
# Create your views here.

# 共用分页逻辑
# 自己实现的分页逻辑(然而并没有什么卵用)
# 匹配当前页 index == (x for x in 总页数)
# def pange_index(goods, index):
#     index = int(index)
#     if int(index) <= 0:
#         index = 1
#     try:
#         goods_counts = goods.objects.count()
#         counts_index = math.ceil(goods_counts / 10)
#         if index >= counts_index:
#             index = counts_index
#             index_page = goods.objects.all()[(index - 1) * 10:]
#         else:
#             index_page = goods.objects.all()[(index - 1) * 10 : index * 10]
#     except DatabaseError as e:
#         logging.warning(e)
#     return index_page, counts_index


# 抽象出的通用的分页逻辑
def page_index(goods, index, Type):
    if not Type:
        contact_list = goods.objects.all()
    else:
        goods_type = get_object_or_404(GoodsType,title=Type)
        contact_list = goods_type.goods_set.all()
    # 目前来看的效果
    paginator = Paginator(contact_list, 10, 2)
    p_totalpage = paginator.page_range
    try:
        good_contact = paginator.page(index)
    except PageNotAnInteger:
        good_contact = paginator.page(1)
    except EmptyPage:
        good_contact = paginator.page(paginator.num_pages)

    return good_contact


# 首页的展示逻辑 待优化(ajax)
def index(request):
    try:
        good_fruit_type = get_object_or_404(GoodsType, title='新鲜水果')
        fruit_goods = random.sample(list(good_fruit_type.goods_set.all()), 4)
        good_fruit_meet = get_object_or_404(GoodsType, title='精品肉类')
        meet_goods = random.sample(list(good_fruit_meet.goods_set.all()), 4)
        good_fruit_water = get_object_or_404(GoodsType, title='海鲜水产')
        water_goods = random.sample(list(good_fruit_water.goods_set.all()), 4)
        vagetables_good_type = get_object_or_404(GoodsType, title='新鲜蔬菜')
        vegetables_good = random.sample(list(vagetables_good_type.goods_set.all()), 4)
        quick_snacks_good = get_object_or_404(GoodsType, title='速冻食品')
        quick_food = random.sample(list(quick_snacks_good.goods_set.all()), 4)
        egg_goods_type = get_object_or_404(GoodsType, title='禽类蛋品')
        eggs_foods = random.sample(list(egg_goods_type.goods_set.all()), 4)
        content = {'fruit_goods': fruit_goods, 'meet_goods': meet_goods, 'water_goods': water_goods, 'vegetables_good': vegetables_good, 'quick_food':quick_food, 'eggs_foods':eggs_foods}
    except DatabaseError as e:
        logging.warning(e)

    user_id = request.session.get('user_id')
    if user_id:
        mycartc = CartInfo.objects.filter(user=user_id).count()
        cart_foods = {'mycartc': mycartc}
    return render(request, 'index.html', {'good_list': locals()})


# 商品列表页的展示逻辑(代码的复用性)
def prolist_list(request, Type=None):
    idv = request.GET.get('page')
    if request.GET.get('Type'):
        Type = request.GET.get('Type')[:-1]
    try:
        goods_list = page_index(Goods, idv, Type)
        hot_goods = random.sample(list(Goods.objects.all()), 2)
    #    page_content = {'goods_list': goods_list, 'hot_goods' : hot_goods}
        # 页面上现实的上一页和下一页是被urlEncode转码的
    except DatabaseError as e:
        logging.warning(e)

    return render(request, 'list.html', {'content': locals()})


# show the good's detail
def deatil_one(request):
    good_id = request.GET.get('good')[:-1]
    try:
        good = Goods.objects.get(id=good_id)
        good_type = good.type
        hot_good = good_type.goods_set.order_by('-id').all()[:2]
        # Typefood = GoodsType.objects.order_by(id='id')
    except ObjectDoesNotExist as e:
        logging.warning(e)
    if request.COOKIES.get('Recently_Viewed'):
        cookie_good = request.COOKIES.get('Recently_Viewed')
        list_good = cookie_good.split(',')
        if good.id in list_good:
            list_good.remove(good.id)
        # 如果最近浏览多的话那么将最久没有被浏览的那个商品删除
        if len(list_good) >= 5:
            list_good.pop()
        list_good = [good_id] + list_good
        cookie_good_new = ','.join(list_good)
    else:
        cookie_good_new = good_id
    user_id = request.session.get('user_id')
    mycartc = 0
    if user_id:
        mycartc = CartInfo.objects.filter(user=user_id).count()

    # cookie处理数据添加的位置
    response = render(request, 'detail.html', {'goodone': good, 'hot_list': hot_good, 'mycartc':mycartc})
    response.set_cookie('Recently_Viewed', cookie_good_new, max_age=3000)
    return response


