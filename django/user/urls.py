from django.urls import path
from user import views

urlpatterns = [
    path("friendlist/", views.friendlist, name="Friendlist"),
    path("friend-invites/", views.friendInvites, name="Friend Invites"),
]
