from django.shortcuts import render
from .models import User, Game, Tournament
from rest_framework import viewsets
from .serializers import UserSerializer, GameSerializer, TournamentSerializer
from rest_framework.permissions import IsAuthenticated


def menu(request):
    return render(request, 'menu/index.html')


def game(request):
    return render(request, 'game/index.html')


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
