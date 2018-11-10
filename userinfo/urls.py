
from django.conf.urls import url,include
from django.contrib import admin
from userinfo import views


urlpatterns = [
    url('^login/', views.signin, name='login'),
    url('^register/', views.register_in, name='register'),
    url('^reigseterin/', views.register_, name='register_in'),
    url('^loginin/', views.login_, name='login_in'),
    url('^loginout/', views.login_out, name='login_out'),
    url('^info/$', views.user_info, name='user_info'),
    url('^useraddress/$', views.user_address, name='useraddress'),
    url('^addads/$', views.add_ads, name='addads'),
    url('^editads/$', views.edit_ads, name='editads'),
    url('^deleteads/$', views.delete_ads, name='deleteads'),


]