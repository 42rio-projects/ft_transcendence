import chat.views as views
from django.urls import path
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'api/chat', views.ChatViewSet)
router.register(r'api/message', views.MessageViewSet)

urlpatterns = [
    path("chat/", views.chat_list, name="chat"),
    path("chat/<int:chat_id>", views.chat, name="chat"),
]

urlpatterns += router.urls
