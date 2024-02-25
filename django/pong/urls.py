from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("game/", views.Game.as_view(), name="game"),
    path("api/twilio", views.TwilioEndpoint.as_view(), name="send_sms"),
    path('api/token', jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh', jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),
    path("menu/", views.Menu.as_view(), name="menu"),
    path("loadscreen/", views.Loadscreen.as_view(), name="loadscreen"),
    path("leaderboard/", views.Leaderboard.as_view(), name="leaderboard"),
	path("cadastro/", views.Cadastro.as_view, name = "cadastro"),
    path("api/users", views.UserEndpoint.as_view(), name="users"),
    path("api/games", views.GameEndpoint.as_view(), name="games"),
    path(
        "api/tournaments",
        views.TournamentEndpoint.as_view(),
        name="tournaments"
    ),
]
