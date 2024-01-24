from django.urls import path, include
from rest_framework import routers
import pong.views as views

router = routers.DefaultRouter()

router.register(r'api/users', views.UserViewSet)
router.register(r'api/games', views.GameViewSet)
router.register(r'api/tournaments', views.TournamentViewSet)

urlpatterns = [
    path("", views.index, name="index"),
    path('', views.menu, name='menu'),
    path('game/', views.game, name='game'),
    path("loadscreen/", views.loadscreen, name="loadscreen"),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path('', include(router.urls)),
]

urlpatterns += router.urls
