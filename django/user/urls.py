from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('upload_avatar', views.upload_avatar, name='upload_avatar'),
    path('change_password', views.change_password, name='change_password'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('verify_email/', views.verify_email, name='verify_email'),
    path('receive_email_code/', views.receive_email_code,
         name='receive_email_code'),
    path('confirm_email_code/', views.confirm_email_code,
         name='confirm_email_code'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
