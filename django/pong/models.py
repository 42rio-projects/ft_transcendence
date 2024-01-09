from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Tournament(models.Model):
    name = models.CharField(max_length=20)
    end = models.DateField(auto_now_add=True)


class Game(models.Model):
    winner = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name='wins')
    loser = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name='losses')
    winner_points = models.PositiveSmallIntegerField()
    loser_points = models.PositiveSmallIntegerField()
    end = models.DateField(auto_now_add=True)
    tournament = models.ForeignKey(
        Tournament, null=True, on_delete=models.SET_NULL, related_name="games")
