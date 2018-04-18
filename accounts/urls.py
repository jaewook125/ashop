from django.urls import path, reverse_lazy
from django.contrib.auth.views import login, logout
from . import views

app_name = 'accounts'

urlpatterns = [
	path('signup', views.signup, name='signup'),
	path('login/', login, name='login', kwargs={
			'template_name' : 'accounts/login_form.html',
		}),
	path('profile/', views.profile, name='profile'),
	path('logout/', logout, name='logout', kwargs={
			'next_page':reverse_lazy('root'),
		}),
]