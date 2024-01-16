from django.shortcuts import render
from django.contrib.auth.models import User
from pong.models import Game
from pong.models import Tournament
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer, GameSerializer, TournamentSerializer


def menu(request):
    return render(request, "menu/index.html")


def game(request):
    return render(request, "game/index.html")


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)  # Chage this to a more secure permission
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GameViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class TournamentViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
