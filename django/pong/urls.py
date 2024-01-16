from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("game/", views.game, name="game"),
	path("menu/", views.menu, name = "menu"),
	path("loadscreen/", views.loadscreen, name = "loadscreen"),
	path("leaderboard/", views.leaderboard, name = "leaderboard"),
    path("api/users", views.UserEndpoint.as_view(), name="users"),
    path("api/games", views.GameEndpoint.as_view(), name="games"),
    path(
        "api/tournaments",
        views.TournamentEndpoint.as_view(),
        name="tournaments"
    ),
]
