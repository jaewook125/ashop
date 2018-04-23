from django.contrib import admin
from .models import Item, Order
from django.utils.safestring import mark_safe

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
	list_display = ['photo_tag','name','amount']
	list_display_links = ['name']
	search_fields = ['name']

	def photo_tag(self, item): 
	#list_display에 지정된 필드명이 멤버함수로 지정되있으면
	#테이블상의 각각의 레코드에 해당 필드값을 취함
		if item.photo:
			return mark_safe('<img src="{}" style="width:70px;"/>'.format(item.photo.url))
			#self str이 안되어있어서 태그가 이스케이프 되있다
			#이경우에는 mark_safe를 사용한다
		return None


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ['imp_uid', 'user', 'name', 'amount_html', 'status_html', 'paid_at', 'receipt_link']