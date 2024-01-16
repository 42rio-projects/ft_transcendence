from rest_framework import serializers
from .models import User, Game, Tournament


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = '__all__'


class GameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'


class TournamentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tournament
        fields = '__all__'
