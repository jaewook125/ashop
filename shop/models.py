from uuid import uuid4 #32글자 랜덤생성
from django.db import models
from django.conf import settings
from iamport import Iamport
from jsonfield import JSONField

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
	meta = JSONField(blank=True, default={})
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	class Meta:
		ordering = ('-id',)

	@property
	def api(self):
		'Iamport Client 인스턴스'
		return Iamport(settings.IAMPORT_API_KEY, settings.IAMPORT_API_SECRET)

	def update(self, commit=True, meta=None):
		'결제내역 갱신'
		if self.imp_uid: #imp_uid에 응답을 받으면
			self.meta = meta or self.api.find(imp_uid=self.imp_uid) #merchant_uid는 반드시 매칭되어야함.
			assert str(self.merchant_uid) == self.meta['merchant_uid']
			#반드시 같아야한다 assert[단언하다]

			self.status = self.meta['status']
		if commit:
			self.save()