from django.urls import path, include
from rest_framework import routers
from .views import menu, game, UserViewSet, GameViewSet, TournamentViewSet

router = routers.DefaultRouter()

router.register(r'api/users', UserViewSet)
router.register(r'api/games', GameViewSet)
router.register(r'api/tournaments', TournamentViewSet)

urlpatterns = [
    path('', menu, name='menu'),
    path('game/', game, name='game'),
    path('', include(router.urls)),
]

urlpatterns += router.urls
