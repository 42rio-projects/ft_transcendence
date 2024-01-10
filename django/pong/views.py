from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Game
from .models import Tournament
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from .utils.pong_game import get_game_instances
from .utils.pong_game import create_game


def menu(request):
    return render(request, "menu/index.html")


def game(request):
    return render(request, "game/index.html")


class UserEndpoint(APIView):
    def get(self, request, format=None):
        try:
            users = User.objects.all()
            return Response(users.values())
        except User.DoesNotExist as e:
            return Response({"error": str(e)}, 404)
        except Exception as e:
            return Response({"error": str(e)}, 500)

    def post(self, request, format=None):
        try:
            user = User(username=request.data["username"],
                        password=request.data["password"])
            user.save()
            return Response({"created": user.username})
        except IntegrityError as e:
            return Response({"error": str(e)}, 409)
        except Exception as e:
            return Response({"error": str(e)}, 500)

    def delete(self, request, format=None):
        try:
            user = User.objects.get(
                username=request.data["username"],
                password=request.data["password"])
            user.delete()
            return Response({"deleted": user.username})
        except User.DoesNotExist as e:
            return Response({"error": str(e)}, 404)
        except Exception as e:
            return Response({"error": str(e)}, 500)


class GameEndpoint(APIView):
    def get(self, request, format=None):
        try:
            return Response(get_game_instances(), 200)
        except Game.DoesNotExist as e:
            return Response(f"{str(e)}", 200)
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


class TournamentEndpoint(APIView):
    def get(self, request, format=None):
        try:
            tournaments = Tournament.objects.all()
            return Response(tournaments.values())
        except Game.DoesNotExist as e:
            return Response({"error": str(e)}, 404)
        except Exception as e:
            return Response({"error": str(e)}, 500)

    def post(self, request, format=None):
        try:
            name = request.data["name"]
            tournament = Tournament(name=name)
            tournament.save()
            return Response({"created": tournament.name})
        except Exception as e:
            return Response({"error": str(e)}, 400)
