from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db import IntegrityError
from pong.utils.pong_game import get_game_instances, create_game, delete_game
from pong.utils.pong_tournament import get_tournaments, create_tournament, delete_tournament
from pong.utils.user import get_users, create_user, delete_user
from .services import send_twilio_code, check_twilio_code
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
import pong.models as models


class Menu(APIView):
    def get(self, request, format=None):
        return render(request, "menu.html")


class Game(APIView):
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

def cadastro(request):
    return render(request, "cadastro.html")

class UserEndpoint(APIView):
    def get(self, request, format=None):
        try:
            return Response(get_users(), 200)
        except Exception as e:
            return Response(str(e), 500)

    def post(self, request, format=None):
        try:
            create_user(request.data)
            return Response("User created.", 200)
        except IntegrityError as e:
            return Response(str(e), 409)
        except Exception as e:
            return Response(str(e), 500)

    def delete(self, request, format=None):
        try:
            delete_user(request.data)
            return Response("User deleted.", 200)
        except IntegrityError as e:
            return Response(str(e), 403)
        except User.DoesNotExist as e:
            return Response(str(e), 404)
        except Exception as e:
            return Response(str(e), 500)


class GameEndpoint(APIView):
    def get(self, request, format=None):
        try:
            return Response(get_game_instances(), 200)
        except Exception as e:
            return Response(str(e), 500)

    def post(self, request, format=None):
        try:
            create_game(request.data)
            return Response("Game created.", 200)
        except models.Tournament.DoesNotExist as e:
            return Response(str(e), 400)
        except Exception as e:
            return Response(str(e), 500)

    def delete(self, request, format=None):
        try:
            delete_game(request.data)
            return Response("Game deleted.", 200)
        except KeyError as e:
            return Response(str(e), 400)
        except Game.DoesNotExist as e:
            return Response(str(e), 404)
        except Exception as e:
            return Response(str(e), 500)


class TournamentEndpoint(APIView):
    def get(self, request, format=None):
        try:
            return Response(get_tournaments())
        except Exception as e:
            return Response(str(e), 500)

    def post(self, request, format=None):
        try:
            create_tournament(request.data)
            return Response("Tournament created.", 200)
        except KeyError as e:
            return Response(str(e), 400)
        except IntegrityError as e:
            return Response(str(e), 409)
        except Exception as e:
            return Response(str(e), 500)

    def delete(self, request, format=None):
        try:
            delete_tournament(request.data)
            return Response("Tournament deleted.", 200)
        except KeyError as e:
            return Response(str(e), 400)
        except models.Tournament.DoesNotExist as e:
            return Response(str(e), 404)
        except Exception as e:
            return Response(str(e), 500)
