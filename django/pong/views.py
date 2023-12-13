from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response


def menu(request):
    return render(request, "menu/index.html")


def game(request):
    return render(request, "game/index.html")


class User(APIView):
    def get(self, request, format=None):
        return Response({"method": "get", "data": request.data})

    def post(self, request, format=None):
        return Response({"method": "post", "data": request.data})


class Game(APIView):
    def get(self, request, format=None):
        return Response({"method": "get", "data": request.data})

    def post(self, request, format=None):
        return Response({"method": "post", "data": request.data})
