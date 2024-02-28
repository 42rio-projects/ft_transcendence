from django.urls import path
from django.contrib.auth import views as auth_views
from login import views

urlpatterns = [
	path("", auth_views.LoginView.as_view(), name='login'),
	path('register/', views.register, name='register'),
]
