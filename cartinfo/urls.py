# python3
from django.conf.urls import url
from cartinfo import views
from django.views.generic import TemplateView

urlpatterns= [
    url('^$', views.cart_info,name='cart'),
    url('^addcart', views.add_cart),
    url('^deletecart', views.delete_cart),
    url('^cartcount', views.cart_count),
    url('^addorder', views.add_order),
    url('^orderlist', views.order_list,name='orderlist'),
    url('^placeorder', views.place_order,name='placeorder'),

]
