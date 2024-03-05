from django.urls import path
from user import views

urlpatterns = [
    path("friendlist/", views.friendlist, name="friendlist"),
    path("friend-invites/", views.friendInvites, name="friendInvites"),
    path(
        "friend-invites/<int:invite_id>/",
        views.respondInvite,
        name="respondInvite"
    ),
    path(
        "send-invite",
        views.sendInvite,
        name="sendInvite"
    ),
]
