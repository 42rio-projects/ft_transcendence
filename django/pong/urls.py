from django.urls import path
from rest_framework import routers
from . import views
from rest_framework_simplejwt import views as jwt_views

router = routers.DefaultRouter()

router.register(r'api/users', views.UserViewSet)
router.register(r'api/games', views.GameViewSet)
router.register(r'api/tournaments', views.TournamentViewSet)

urlpatterns = [
    path('', views.MenuView.as_view(), name='menu'),
    path('game/', views.GameView.as_view(), name='game'),
    path('api/twilio', views.TwilioEndpoint.as_view(), name='send_sms'),
    path('api/token', jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh', jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),
    path('menu/', views.MenuView.as_view(), name='menu'),
    path('loadscreen/', views.loadscreen, name='loadscreen'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]

urlpatterns += router.urls
