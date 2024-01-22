from django.shortcuts import render
from django.template import loader
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
import django.http as http
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


def chat_list(request):
    chats = models.Chat.objects.all()  # Should filter by chats the user is in
    template = loader.get_template("pong/chat_list.html")
    context = {
        "chats": chats,
    }
    return http.HttpResponse(template.render(context, request))


def chat(request, chat_id):
    try:
        chat = models.Chat.objects.get(id=chat_id)
    except models.Chat.DoesNotExist:
        raise http.Http404("Chat does not exist")
    template = loader.get_template("pong/chat.html")
    context = {
        "chat": chat,
    }
    return http.HttpResponse(template.render(context, request))


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


class ChatViewSet(viewsets.ModelViewSet):
    queryset = models.Chat.objects.prefetch_related('messages')
    serializer_class = serializers.ChatSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['PUT'])
    def add(self, request, pk=None):
        chat = self.get_object()
        serializer = serializers.UsernameSerializer(data=request.data)
        if not serializer.is_valid():
            raise Exception("Invalid json")  # Define better behavior here
        user = models.User.objects.get(
            username=serializer.validated_data["username"])
        chat.add_user(user)
        return Response({'status': 'user added'})

    @action(detail=True, methods=['PUT'])
    def remove(self, request, pk=None):
        chat = self.get_object()
        serializer = serializers.UsernameSerializer(data=request.data)
        if not serializer.is_valid():
            raise Exception("Invalid json")  # Define better behavior here
        user = models.User.objects.get(
            username=serializer.validated_data["username"])
        chat.remove_user(user)
        return Response({'status': 'user removed'})


class MessageViewSet(viewsets.ModelViewSet):
    queryset = models.Message.objects.all()
    serializer_class = serializers.MessageSerializer
    permission_classes = [IsAuthenticated]
