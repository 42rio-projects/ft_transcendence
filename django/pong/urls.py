from django.urls import path
from . import views

urlpatterns = [
    path("", views.menu, name="menu"),
    path("game/", views.game, name="game"),
    path("api/users", views.User.as_view(), name="users"),
    path("api/games", views.Game.as_view(), name="games"),
]
