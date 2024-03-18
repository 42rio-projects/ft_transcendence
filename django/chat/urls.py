import chat.views as views
from django.urls import path
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'api/chat', views.ChatViewSet)
router.register(r'api/message', views.MessageViewSet, basename='message')

urlpatterns = [
    path("chat/", views.chatIndex, name="chatIndex"),
    path("chat/list", views.chatList, name="chatList"),
    path("chat/new-chat", views.startChat, name="startChat"),
    path("chat/<int:id>", views.chatRoom, name="chatRoom"),
    path("chat/<str:room_name>/", views.room, name="room"),
]

urlpatterns += router.urls
