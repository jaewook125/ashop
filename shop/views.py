from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from .models import Item, Order
from .forms import PayForm

class ItemListView(ListView):
	model=Item
	queryset=Item.objects.filter(is_public=True)

	def get_queryset(self):
		self.q = self.request.GET.get('q','') #q가 있으면 넣고 없으면 공백

		qs = super().get_queryset() #기본 쿼리셋을 하나 긁어내고
		if self.q:
			qs = qs.filter(name__icontains=self.q) #name에서 self.q가 있으면 필터링한다
		return qs

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['q'] = self.q #content에다 q라는 이름으로 self.q에 저장하겠다

		return context
index = ItemListView.as_view()

@login_required
def order_new(request, item_id): #특정 아이템 하나만 지정해서 name,amount를 활용한다
	item = get_object_or_404(Item, pk=item_id) #아이템을 획득해옴
	order = Order.objects.create(user=request.user, item=item, name=item.name, amount=item.amount)
	return redirect('shop:order_pay', item_id, str(order.merchant_uid))

@login_required
def order_pay(request, item_id, merchant_uid):
	order = get_object_or_404(Order, user=request.user, merchant_uid=merchant_uid, status='ready')
	if request.method == "POST":
		form = PayForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('accounts:profile')
	else:
		form = PayForm(instance=order)
	return render(request, 'shop/pay_form.html', {
			'form':form,
		})