import json
from django.utils.safestring import mark_safe
from django.utils.encoding import smart_text
from django.template.loader import render_to_string
from django import forms
from .models import Order


# class OrderForm(forms.ModelForm):
# 	#각각의 모델필드로부터 폼필드를 생성
# 	class Meta:
# 		model = Order
# 		fields = ('name','amount') #유저가 값을 바꿀수있다 조심, readonly <-읽기 전용
# 		#각각의 폼필드에는 기본 정의된 위젯이 있다 ex)forms.TextInput
# 		widgets = {
# 			'name' :forms.TextInput(attrs={'readonly':'readonly'}),
# 			'amount':forms.TextInput(attrs={'readonly':'readonly'})
# 			#폼필드 재정의 ex) <input type="text" readonly="readonly" />
# 		}

class PayForm(forms.ModelForm):
	class Meta:
		model = Order
		fields = ('imp_uid',)

	def as_iamport(self):
		# 본 Form의 Hidden 필드 위젯
		hidden_fields = mark_safe(''.join(smart_text(field) for field in self.hidden_fields())) #안전한 문자열
		# IMP.request_pay의 인자로 넘길 인자 목록
		fields = {
			'merchant_uid': str(self.instance.merchant_uid), ##uuid4에 리턴 값에대한 객체
			'name': self.instance.name,
			'amount': self.instance.amount,
		}
		return hidden_fields + render_to_string('shop/_iamport.html', {
			'json_fields': mark_safe(json.dumps(fields, ensure_ascii=False)), 
			#json으로 직렬화 한 후 
			'iamport_shop_id': 'iamport', # FIXME: 각자의 상점 아이디로 변경 가능
		})

	def save(self):
		order = super().save(commit=False)
		order.status = 'paid' # FIXME: 아임포트 API를 통한 확인 후에 변경을 해야만 합니다.
		order.save()
		return order