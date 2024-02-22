import json
import chat.models as models
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.serializers import MessageSerializer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        try:
            data_json = json.loads(text_data)
            content = data_json['content']
            user = await get_user(data_json['user'])
            chat = await get_chat(data_json['chat_name'])
            message = await create_message(content, user, chat)
            message_data = await message_to_dict(message)
        except Exception as e:
            print(e)
            await self.send(text_data=json.dumps({
                'type': 'error',
                'content': 'Unable to send message.',
            }))
            return
        message_data['type'] = 'chat.message'

        # Send message to room group
        await self.channel_layer.group_send(self.room_group_name, message_data)

    # Receive message from room group
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))


@database_sync_to_async
def get_chat(chat_name):
    chat = models.Chat.objects.get(name='chat_name')
    return chat


@database_sync_to_async
def get_user(username):
    user = models.User.objects.get(username=username)
    return user


@database_sync_to_async
def create_message(content, user, chat):
    message = models.Message.objects.create(
        content=content, sender=user, chat=chat
    )
    message.save()
    return message


@sync_to_async
def message_to_dict(message):
    return MessageSerializer(message).data
