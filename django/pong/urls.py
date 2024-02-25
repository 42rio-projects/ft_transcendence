from django.urls import path
from rest_framework import routers
import pong.views as views
from rest_framework_simplejwt import views as jwt_views

router = routers.DefaultRouter()

router.register(r'api/users', views.UserViewSet)
router.register(r'api/games', views.GameViewSet)
router.register(r'api/tournaments', views.TournamentViewSet)

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
	path("cadastro/", views.Cadastro.as_view(), name = "cadastro"),
]

urlpatterns += router.urls
