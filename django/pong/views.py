from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
import pong.serializers as serializers
import pong.models as models


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
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]


class GameViewSet(viewsets.ModelViewSet):
    queryset = models.Game.objects.all()
    serializer_class = serializers.GameSerializer
    permission_classes = [IsAuthenticated]


class TournamentViewSet(viewsets.ModelViewSet):
    queryset = models.Tournament.objects.all()
    serializer_class = serializers.TournamentSerializer
    permission_classes = [IsAuthenticated]
