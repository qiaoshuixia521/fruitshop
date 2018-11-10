#-*- coding: UTF-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.http import request, response
from django.contrib import messages
from django.db import DatabaseError
import logging
import json
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from memberapp.models import Goods
# Create your views here.
from hashlib import sha1

# get请求
auth_check = 'MarcelArhut'


# 装饰器(面向切面， 对于某些页面进行装饰， 要求进行权限认证, 并且记录跳转前的位置值)
def login_decorator(func):
    def login_func(request, *args, **kwargs):
        # if request.session.get('user_id', None):...
        if request.session.get('user_name', None):
            return func(request, *args, **kwargs)
        else:
            response = redirect('/user/login/')
            response.set_cookie('url', request.path)
            return response
    return login_func

# 清除Cookies中的数据转存到Session中(购物车啊)


# 拦截器2 如果已经登录过那么首先跳转到原页面 或者跳转到原有的页面


# 重定向到登录页
# @login_decorator
def signin(request):
    return render(request, 'login.html')


# 重定向到注册页面
def register_in(request):
    return render(request, 'register.html')


# 处理post请求页面，如果完成重新跳转到对应的页面
def login_(request):
    if request.method == 'POST':
        user = UserInfo()
        user.uname = request.POST.get('username')
        user.upassword = request.POST.get('pwd')
        try:
            find_user = UserInfo.objects.filter(uname=user.uname)
            if len(find_user) <= 0:
                messages.add_message(request, messages.ERROR, '该用户未注册')
                return redirect('/user/login/')
            if not check_password(user.upassword, find_user[0].upassword): #
                return render(request, 'login.html', {'user_info': user, 'message_error': '用户名或者密码错误'})
        except ObjectDoesNotExist as e:
            logging.warning(e)
        request.session['user_id'] = find_user[0].id
        request.session['user_name'] = user.uname
        if request.COOKIES.get('url'):
            url = request.COOKIES.get('url')
            res = redirect(url)
            res.delete_cookie('url')
            return res
        # 购物车的中的数据清空并转存到session当中
        # if request.COOKIES.get('cart'):
        #       request.session['cart'] = request.COOKIES.get('cart')
        #       del request.COOKIES['cart']
        return redirect('/')
    return redirect('/user/login/')


def register_(request):
    if request.method == 'POST':

        new_user = UserInfo()
        new_user.uname = request.POST.get('user_name')
        try:
            a = UserInfo.objects.get(uname=new_user.uname)
            if a:
                return render(request, 'register.html', {'messageuname': '该用户名已经存在'})
        except ObjectDoesNotExist as e:
            logging.warning(e)
        if request.POST.get('pwd') != request.POST.get('cpwd'):
            return render(request, 'register.html', {'message_': '两次输入的密码不一致'})
        new_user_pwd = make_password(request.POST.get('pwd'), auth_check, 'pbkdf2_sha1')
        new_user.upassword = new_user_pwd
        new_user.email = request.POST.get('email')

        try:
            new_user.save()
        except DatabaseError as e:
            logging.warning(e)
        return render(request, 'index.html')
    return redirect('/user/register/')


# 处理的页面信息
def login_out(request):
    try:
        if request.session['user_name']:
            del request.session['user_id']
            del request.session['user_name']
    except KeyError as e:
        logging.warning(e)
    return redirect('/')


# show the user info
@login_decorator
def user_info(request):
    try:
        rec_view_list = list()
        userinfo = get_object_or_404(UserInfo, uname=request.session.get('user_name'))
        user_id = request.session.get('user_id')
        adss = Address()
        adss = Address.objects.filter(user_id=user_id)
        if request.COOKIES.get('Recently_Viewed', None):
            rec_view = request.COOKIES.get('Recently_Viewed', None)
            list_view = rec_view.split(',')
            for i in list_view:
                rec_view_list.append(Goods.objects.get(id=i))
        else:
            rec_view_list = []
    except ObjectDoesNotExist as e:
        logging.warning(e)
    if len(adss)>0:
        content = {'userinfo': userinfo, 'rec_view': rec_view_list, 'adss':adss[0]}
    else:
        content = {'userinfo': userinfo, 'rec_view': rec_view_list, 'adss':''}
    return render(request, 'user_center_info.html', content)


# show user's address
@login_decorator
def user_address(request):
    user_id = request.session.get('user_id')
    adss = Address.objects.filter(user_id=user_id)
    return render(request, 'user_center_site.html', {'adss': adss})


# add a new address
@login_decorator
def add_ads(request):
    user_id = request.session.get('user_id')
    addressee = request.POST.get('addressee')
    Detailed_address = request.POST.get('Detailed_address')
    cellphone = request.POST.get('cellphone')
    try:
        userd_ = UserInfo.objects.get(id=user_id)
        Address.objects.create(aname=addressee, address=Detailed_address, cellphone=cellphone, user=userd_)
    except ObjectDoesNotExist as e:
        logging.warning(e)
    return redirect('useraddress')


# delete id=adid address
@login_decorator
def delete_ads(request):
    user_id = request.session.get('user_id')
    adid = request.GET.get('adid')
    try:
        delads = Address.objects.get(user_id=user_id, id=adid)
        delads.delete()
    except BaseException as e:
        logging.warning(e)

    return redirect('useraddress')


# add a new address
@login_decorator
def edit_ads(request):
    user_id = request.session.get('user_id')
    ida = request.POST.get('ida')
    addressee = request.POST.get('addresseed')
    Detailed_address = request.POST.get('Detailed_addressd')
    cellphone = request.POST.get('cellphoned')
    try:
        Address.objects.filter(id=ida).update(aname=addressee, address=Detailed_address, cellphone=cellphone)
    except ObjectDoesNotExist as e:
        logging.warning(e)
    return redirect('useraddress')
