from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path("", views.Menu.as_view(), name="menu"),
    path("game/", views.Game.as_view(), name="game"),
    path("api/twilio", views.TwilioEndpoint.as_view(), name="send_sms"),
    path('api/token', jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh', jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),
    path("menu/", views.Menu.as_view(), name="menu"),
    path("loadscreen/", views.loadscreen, name="loadscreen"),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
	path("cadastro/", views.cadastro, name = "cadastro"),
    path("api/users", views.UserEndpoint.as_view(), name="users"),
    path("api/games", views.GameEndpoint.as_view(), name="games"),
    path(
        "api/tournaments",
        views.TournamentEndpoint.as_view(),
        name="tournaments"
    ),
]
