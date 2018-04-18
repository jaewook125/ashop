from django.shortcuts import render
from django.views.generic import ListView
from .models import Item

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