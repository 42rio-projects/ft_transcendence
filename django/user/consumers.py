import json

from channels.generic.websocket import AsyncWebsocketConsumer


class statusConsumer(AsyncWebsocketConsumer):
    online_users = []

    async def connect(self):
        """Accept connection and broadcast new online list"""
        await self.channel_layer.group_add('status', self.channel_name)
        await self.accept()
        self.user = self.scope['user']
        self.online_users.append(self.user.username)
        await self.channel_layer.group_send(
            'status', {'type': 'status.update'}
        )

    async def disconnect(self, close_code):
        self.online_users.remove(self.user.username)
        await self.channel_layer.group_send(
            'status', {'type': 'status.update'}
        )
        await self.channel_layer.group_discard('satus', self.channel_name)

    async def receive(self, text_data):
        pass

    async def status_update(self, event):
        """Send updated online list to websocket"""
        await self.send(text_data=json.dumps(
            {"online_users": self.online_users})
        )
