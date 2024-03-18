# import django.http as http
# from django.template import loader
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from user.models import User
import chat.serializers as serializers
import chat.models as models


def chatIndex(request):
    template = loader.get_template('chat/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def chatList(request):
    template = loader.get_template('chat/chatlist.html')
    context = {}
    return HttpResponse(template.render(context, request))
    # chats = Chat.objects.all()  # Should filter by chats the user is in
    # template = loader.get_template("chat/list.html")
    # context = {
    #     "chats": chats,
    # }
    # return http.HttpResponse(template.render(context, request))


def chatRoom(request, id):
    chat = get_object_or_404(models.Chat, pk=id)
    if chat.starter != request.user and chat.receiver != request.user:
        return HttpResponse(status_code=403)
    if request.method == 'POST':
        content = request.POST.get('content')
        try:
            models.Message(
                content=content, sender=request.user, chat=chat
            ).save()
        except Exception as e:
            return HttpResponse(e)
    template = loader.get_template('chat/chat.html')
    context = {"chat": chat}
    return HttpResponse(template.render(context, request))


def startChat(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        user = get_object_or_404(
            User,
            username=name,
        )
        try:
            models.Chat(starter=request.user, receiver=user).save()
            # add 201 response that is not rendered on the front end
        except Exception as e:
            return HttpResponse(e)
    template = loader.get_template("chat/start_chat.html")
    context = {}
    return HttpResponse(template.render(context, request))


def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})
    # try:
    #     chat = Chat.objects.get(id=chat_id)
    # except Chat.DoesNotExist:
    #     raise http.Http404("Chat does not exist")
    # template = loader.get_template("chat/chat.html")
    # context = {
    #     "chat": chat,
    # }
    # return http.HttpResponse(template.render(context, request))


class ChatViewSet(viewsets.ModelViewSet):
    queryset = models.Chat.objects.all()
    serializer_class = serializers.ChatSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['PUT'])
    def add(self, request, pk=None):
        chat = self.get_object()
        serializer = serializers.UsernameSerializer(data=request.data)
        if not serializer.is_valid():
            raise Exception("Invalid json")  # Define better behavior here
        user = User.objects.get(
            username=serializer.validated_data["username"])
        chat.add_user(user)
        return Response({'status': 'user added'})

    @action(detail=True, methods=['PUT'])
    def remove(self, request, pk=None):
        chat = self.get_object()
        serializer = serializers.UsernameSerializer(data=request.data)
        if not serializer.is_valid():
            raise Exception("Invalid json")  # Define better behavior here
        user = User.objects.get(
            username=serializer.validated_data["username"])
        chat.remove_user(user)
        return Response({'status': 'user removed'})


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.MessageSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = models.Message.objects.all().order_by('-date')
        chat_name = self.request.query_params.get('chat')
        if chat_name is not None:
            queryset = queryset.filter(chat=chat_name)
        return queryset
