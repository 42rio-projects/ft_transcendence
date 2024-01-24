from django.shortcuts import render
from .models import User, Game, Tournament
from rest_framework import viewsets, permissions
from .serializers import UserSerializer, GameSerializer, TournamentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import send_twilio_code, check_twilio_code
from rest_framework.decorators import permission_classes, api_view


@permission_classes((permissions.AllowAny,))
class MenuView(APIView):
    def get(self, request, format=None):
        return render(request, "menu.html")


@permission_classes((permissions.AllowAny,))
class GameView(APIView):
    def get(self, request, format=None):
        return render(request, "game.html")


@permission_classes([IsAuthenticated])
class TwilioEndpoint(APIView):
    def post(self, request, format=None):
        to = request.data.get('to')
        channel = request.data.get('channel')
        code = request.data.get('code')

        if to and channel:
            status = send_twilio_code(to, channel)
            return Response({'status': status})
        elif to and code:
            status = check_twilio_code(to, code)
            return Response({'status': status})
        else:
            return Response({'error': 'Invalid request'}, status=400)


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
