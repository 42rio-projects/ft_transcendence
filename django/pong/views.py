from django.shortcuts import render
import pong.serializers as serializers
import pong.models as models
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import send_twilio_code, check_twilio_code
from rest_framework.decorators import permission_classes, action


@permission_classes((permissions.AllowAny,))
class MenuView(APIView):
    def get(self, request, format=None):
        return render(request, "menu.html")

@permission_classes((permissions.AllowAny,))
class GameView(APIView):
    def get(self, request, format=None):
        return render(request, "game.html")

@permission_classes((permissions.AllowAny,))
class Index(APIView):
    def get(self,request, format=None):
        return render(request, "index.html")

@permission_classes((permissions.AllowAny,))
class Menu(APIView):
    def get(self, request, format=None):
        return render(request, "menu.html")

@permission_classes((permissions.AllowAny,))
class Game(APIView):
    def get(self, request, format=None):
        return render(request, "game.html")

@permission_classes((permissions.AllowAny,))
class Loadscreen(APIView):
    def get(self, request, format=None):
        return render(request, "loadscreen.html")

@permission_classes((permissions.AllowAny,))
class Leaderboard(APIView):
    def get(self, request, format=None):
        return render(request, "leaderboard.html")

@permission_classes((permissions.AllowAny,))
class Cadastro(APIView):
    def get(self,request, format=None):
        return render(request, "cadastro.html")

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
    lookup_field = 'name'
    serializer_class = serializers.TournamentSerializer
    permission_classes = [IsAuthenticated]

    # temporary API endpoint to advance tournament
    @action(detail=True, methods=['GET'])
    def advance(self, request, name=None):
        tournament = self.get_object()
        tournament.new_round()
        return Response({'status': 'tournament round advanced'})
