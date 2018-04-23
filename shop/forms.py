import json
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.encoding import smart_text
from django.template.loader import render_to_string
from django import forms
from .models import Order
from .mixins import IamportBaseForm

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

class PayForm(IamportBaseForm):
	template_name = 'shop/_iamport.html'
	params_names = ['merchant_uid', 'name', 'amount']
	imp_fn_name = 'request_pay'

	class Meta:
		model = Order
		fields = ['imp_uid']
		widgets = {
			'imp_uid': forms.HiddenInput,
		}