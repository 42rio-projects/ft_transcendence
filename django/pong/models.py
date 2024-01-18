from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Chat(models.Model):
    name = models.CharField(max_length=20)
    members = models.ManyToManyField(User)

    def add_user(self, user):
        self.members.add(user)

    def remove_user(self, user):
        self.members.remove(user)


class Message(models.Model):
    content = models.CharField()
    date = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name="messages"
    )
    chat = models.ForeignKey(
        Chat, on_delete=models.CASCADE, related_name="messages"
    )


class Tournament(models.Model):
    name = models.CharField(max_length=100, unique=True)
    beginning = models.DateField(auto_now_add=True)
    last_update = models.DateField(auto_now=True)


class Game(models.Model):
    winner = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name='wins')
    loser = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name='losses')
    winner_points = models.PositiveSmallIntegerField()
    loser_points = models.PositiveSmallIntegerField()
    beginning = models.DateField(auto_now_add=True)
    last_update = models.DateField(auto_now=True)
    tournament_round = models.PositiveSmallIntegerField(null=True)
    tournament = models.ForeignKey(
        Tournament, null=True, on_delete=models.SET_NULL, related_name='games')
