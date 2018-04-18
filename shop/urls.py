from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
	path('', views.index, name='index'),
	path('<int:item_id>/order/new', views.order_new, name='order_new'),
]