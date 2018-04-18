from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy #success_url 활용 될때 순차적으로 실행하지않고 "게으르게" 실행
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

signup = CreateView.as_view(model=User, form_class=UserCreationForm,
							template_name='accounts/signup_form.html',
							success_url=reverse_lazy('root')) 
							#success_url이 활용이 될때 root실행



@login_required
def profile(request):
	return render(request, 'accounts/profile.html')
