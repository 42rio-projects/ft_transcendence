import django.http as http
import chat.serializers as serializers
from django.template import loader
from chat.models import Chat, Message, User
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


def chat_list(request):
    chats = Chat.objects.all()  # Should filter by chats the user is in
    template = loader.get_template("chat/chat_list.html")
    context = {
        "chats": chats,
    }
    return http.HttpResponse(template.render(context, request))


def chat(request, chat_id):
    try:
        chat = Chat.objects.get(id=chat_id)
    except Chat.DoesNotExist:
        raise http.Http404("Chat does not exist")
    template = loader.get_template("chat/chat.html")
    context = {
        "chat": chat,
    }
    return http.HttpResponse(template.render(context, request))


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.prefetch_related('messages')
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
    queryset = Message.objects.all()
    serializer_class = serializers.MessageSerializer
    permission_classes = [IsAuthenticated]
