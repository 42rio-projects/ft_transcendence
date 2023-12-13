from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db import IntegrityError


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


class Game(APIView):
    def get(self, request, format=None):
        return Response({"method": "get", "data": request.data})

    def post(self, request, format=None):
        return Response({"method": "post", "data": request.data})
