from uuid import uuid4 #32글자 랜덤생성
from django.db import models
from django.conf import settings

class Item(models.Model):
	name = models.CharField(max_length=100, db_index=True)
	desc = models.TextField(blank=True)
	amount = models.PositiveIntegerField()
	photo = models.ImageField()
	is_public = models.BooleanField(default=False, db_index=True)
	#공개된 아이템
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

class Order(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
	item = models.ForeignKey(Item, on_delete=models.PROTECT)
	merchant_uid = models.UUIDField(default=uuid4, editable=False) #함수를 호출 return을 default로 저장, 수정될수없게 editable 
	imp_uid = models.CharField(max_length=100, blank=True) #iamport측에서 지정
	name = models.CharField(max_length=100, verbose_name="상품명")
	amount = models.PositiveIntegerField(verbose_name="결제금액")
	status = models.CharField(
		max_length=9,
		choices=(
			('ready', '미결제'),
			('paid', '결제완료'),
			('cancelled', '결제취소'),
			('failed', '결제실패'),
		),
		default='ready',
		db_index=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	class Meta:
		ordering = ('-id',)