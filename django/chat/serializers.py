from rest_framework import serializers
from chat.models import Message, Chat
from user.models import User


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()
    chat = serializers.StringRelatedField()

    class Meta:
        model = Message
        fields = '__all__'


class ChatSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Chat
        fields = ['name', 'private', 'members']


class UsernameSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username']
