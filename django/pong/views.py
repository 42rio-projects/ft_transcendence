from django.shortcuts import render
from .models import User, Game, Tournament
from rest_framework import viewsets
from .serializers import UserSerializer, GameSerializer, TournamentSerializer
from rest_framework.permissions import IsAuthenticated


def index(request):
    return render(request, "index.html")


def menu(request):
    return render(request, 'menu.html')


def game(request):
    return render(request, 'game.html')


def loadscreen(request):
    return render(request, "loadscreen.html")


def leaderboard(request):
    return render(request, "leaderboard.html")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [IsAuthenticated]


class TournamentViewSet(viewsets.ModelViewSet):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = [IsAuthenticated]
