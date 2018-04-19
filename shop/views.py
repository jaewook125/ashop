from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from .models import Item
from .forms import OrderForm

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
	initial = {'name':item.name, 'amount':item.amount} #사전

	if request.method == "POST": #모든 view는 POST로 구분된다
		form = OrderForm(request.POST, initial=initial) #모든 폼은 initial이라는 초기값이 있다
		if form.is_valid():
			order = form.save(commit=False) #실제 결제가 되므로 order인스턴스가 생성됐다.
			order.user = request.user
			order.item = item 
			order.save()
			return redirect('accounts:profile')
	else:
		form = OrderForm(initial=initial)

	return render(request, "shop/order_form.html", {
			'form':form,
			'iamport_shop_id':'iamport', #가맹점 식별코드
		})