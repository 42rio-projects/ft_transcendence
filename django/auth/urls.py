from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('receive_code/', views.receive_code, name='receive_code'),
    path('confirm_code/', views.confirm_code, name='confirm_code'),
]
