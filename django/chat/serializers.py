from rest_framework import serializers
from chat.models import User, Message, Chat


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class ChatSerializer(serializers.HyperlinkedModelSerializer):
    messages = MessageSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Chat
        fields = '__all__'


class UsernameSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username']
