from rest_framework import serializers
from pong.models import User, Game, Tournament, Chat, Message
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)


class GameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'


class TournamentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tournament
        fields = '__all__'


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
