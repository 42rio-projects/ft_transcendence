from django.urls import path
from user import views

urlpatterns = [
    path("friendlist/", views.friendlist, name="friendList"),
    path("friends/", views.friends, name="friends"),
    path(
        "friendlist/<int:user_id>",
        views.excludeFriend,
        name="excludeFriend"
    ),
    path("friend-invites/", views.friendInvites, name="friendInvites"),
    path(
        "friend-invites-sent/",
        views.friendInvitesSent,
        name="friendInvitesSent"
    ),
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
