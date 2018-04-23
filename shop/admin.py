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
	actions = ['do_update','do_cancel']

	def do_update(self, request, queryset): #모든 커스텀 admin action은 첫번째인자로 request를 받음
		'주문 정보를 갱신합니다.'
		total = queryset.count()
		if total > 0: #0보다 크면
			for order in queryset: #쿼리셋을 순회하면서
				order.update() #오더 업데이트
			self.message_user(request, '주문 {}건의 정보를 갱신했습니다.'.format(total))
		else:
			self.message_user(request, '갱신할 주문이 없습니다.')
	do_update.short_description = '선택된 주문들의 아임포트 정보 갱신하기'



	def do_cancel(self, request, queryset):
		'선택된 주문에 대해 결제취소요청을 합니다.'
		queryset = queryset.filter(status='paid')
		total = queryset.count()
		if total > 0:
			for order in queryset:
				order.cancel()
			self.message_user(request, '주문 {}건을 취소했습니다.'.format(total))
		else:
			self.message_user(request, '취소할 주문이 없습니다.')
	do_cancel.short_description = '선택된 주문에 대해 결제취소요청하기'