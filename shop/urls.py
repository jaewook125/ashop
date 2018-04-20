from django.urls import path, re_path
from . import views

app_name = 'shop'

urlpatterns = [
	path('', views.index, name='index'),
	path('<int:item_id>/order/new', views.order_new, name='order_new'),
	re_path(r'^(?P<item_id>\d+)/order/(?P<merchant_uid>[\da-f\-]{36})/pay/$', views.order_pay, name='order_pay'),
]