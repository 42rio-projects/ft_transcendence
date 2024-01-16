from django.urls import path, include
from rest_framework import routers, authtoken
from pong.views import menu, game, UserViewSet, GameViewSet, TournamentViewSet

router = routers.DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'games', GameViewSet)
router.register(r'tournaments', TournamentViewSet)

urlpatterns = [
    path('', menu, name='menu'),
    path('game/', game, name='game'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path("api-token-auth/", authtoken.views.obtain_auth_token),
]
