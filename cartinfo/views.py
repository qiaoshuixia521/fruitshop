#-*- coding: UTF-8 -*-
from django.shortcuts import render, redirect
from django.http import request, response, HttpResponse

from userinfo.views import login_decorator
from django.db import DatabaseError
from cartinfo.models import CartInfo, Order
import logging
import json
import datetime
import random
from memberapp.models import Goods
from userinfo.models import UserInfo, Address


from django.http import JsonResponse


@login_decorator
def cart_info(request):
    user_id = request.session.get('user_id')
    find_goods = CartInfo.objects.filter(user=user_id)

    user_id = request.session.get('user_id')
    mycartc = 0
    if user_id:
        mycartc = CartInfo.objects.filter(user=user_id).count()

    return render(request, 'cart.html', {'find_goods': find_goods,'mycartc':mycartc})


# the cart count
@login_decorator
def cart_count(request):
    user_id = request.session.get('user_id')
    mycartc = CartInfo.objects.filter(user=user_id).count()
    cart_foods = {'mycartc': mycartc}
    return HttpResponse(json.dumps(cart_foods))


# add a new cart,the cart detail and count and other things will be save
@login_decorator
def add_cart(request):

    new_cart = CartInfo()
    user_id = request.session.get('user_id')
    good_id = request.GET.get('good_id')
    good_count = request.GET.get('gcount')
    good_ = Goods.objects.filter(id=good_id)
    user_ = UserInfo.objects.get(id=user_id)
    if len(good_) > 0:
        new_cart.user = user_
        new_cart.good = good_[0]
    else:
        print ('添加购物车失败')
        redirect('/cart/')

    new_cart.ccount = int(good_count)
    try:
        oldgo = CartInfo.objects.filter(good_id=good_id, user_id=user_id)
        if len(oldgo)>0:
            oldgo[0].ccount = oldgo[0].ccount + int(good_count)
            oldgo[0].save()
            # or you can write with :CartInfo.objects.filter(id=oldgo.id).update(ccount=sccount )
        else:
            new_cart.save()
    except BaseException as e:
        logging.warning(e)
        print ('数据库插入异常')
        content = {'status': 'Ok', 'text': '添加数据失败'}
        return HttpResponse(json.dumps(content))
    content = {'status': 'Ok', 'text': '添加数据成功'}
    # return HttpResponse(json.dumps(content), content_type='application/json')
    return HttpResponse(json.dumps(content))


# delete the id=cart_id raw
@login_decorator
def delete_cart(request):

    user_id = request.session.get('user_id')
    cart_id = request.GET.get('cart_id')
    try:
        delcart = CartInfo.objects.filter(user_id=user_id, id=cart_id)
        delcart.delete()
    except BaseException as e:
        logging.warning(e)
    content = {'status': 'Ok', 'text': '删除成功'}
    return HttpResponse(json.dumps(content))


# add a new order , ads is means address ,cals means the goods which is selected,acot  means the count of goods
@login_decorator
def add_order(request):

    user_id = request.session.get('user_id')
    ads = request.POST.get('ads')
    cals = request.POST.get('cals')
    acot = request.POST.get('acot')
    acounts = request.POST.get('acounts')
    orderTime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    try:
        userd_ = UserInfo.objects.get(id=user_id)
        Order.objects.create(user=userd_, orderNo=orderTime, ads=ads, acot=acot, acounts=acounts, cals=cals)
    except BaseException as e:
        logging.warning(e)
    content = {'status': 'Ok', 'text': '删除成功'}
    return HttpResponse(json.dumps(content))

#show the order list
@login_decorator
def order_list(request):
    user_id = request.session.get('user_id')
    orders = Order.objects.filter(user=user_id)
    for order in orders:
        order.cals = json.loads(order.cals)
    return render(request, 'user_center_order.html', {'orders': orders})

#show order's address
@login_decorator
def place_order(request):
    user_id = request.session.get('user_id')
    adss = Address.objects.filter(user_id=user_id)
    content = {'adss': adss}
    return render(request, 'place_order.html', content)