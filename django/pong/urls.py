from django.urls import path
from . import views

urlpatterns = [
    path("", views.menu, name="menu"),
    path("game/", views.game, name="game"),
]
