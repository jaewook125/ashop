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
	name = models.CharField(max_length=100, verbose_name="상품명")
	amount = models.PositiveIntegerField(verbose_name="결제금액")
