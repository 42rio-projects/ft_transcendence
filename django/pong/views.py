from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from pong.models import Game
from pong.models import Tournament
from django.db import IntegrityError
from pong.utils.pong_game import get_game_instances
from pong.utils.pong_game import create_game
from pong.utils.pong_game import delete_game
from pong.utils.pong_tournament import get_tournaments
from pong.utils.pong_tournament import create_tournament
from pong.utils.pong_tournament import delete_tournament
from pong.utils.user import get_users
from pong.utils.user import create_user
from pong.utils.user import delete_user


def index(request):
    return render(request, "index.html")

def game(request):
    return render(request, "game.html")

def menu(request):
    return render(request, "menu.html")

def loadscreen(request):
    return render(request, "loadscreen.html")

def leaderboard(request):
    return render(request, "leaderboard.html")

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
        except Tournament.DoesNotExist as e:
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
        except Tournament.DoesNotExist as e:
            return Response(str(e), 404)
        except Exception as e:
            return Response(str(e), 500)
