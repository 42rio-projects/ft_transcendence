from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('verify_email/', views.verify_email, name='verify_email'),
    path('receive_email_code/', views.receive_email_code,
         name='receive_email_code'),
    path('confirm_email_code/', views.confirm_email_code,
         name='confirm_email_code'),
]
