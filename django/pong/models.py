from django.db import models
from django.contrib.auth.models import User


class Tournament(models.Model):
    name = models.CharField(max_length=100, unique=True)
    date = models.DateField(auto_now_add=True)
    players = models.ManyToManyField(User, related_name='tournaments')
    winner = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name='championships'
    )


class Round(models.Model):
    tournament = models.ForeignKey(
        Tournament,
        related_name='rounds',
        on_delete=models.CASCADE
    )
    number = models.PositiveSmallIntegerField()


class Game(models.Model):
    player_1 = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name='home_games'
    )
    player_2 = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name='away_games'
    )
    round = models.ForeignKey(
        Round,
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
        related_name='games'
    )
    date = models.DateField(auto_now_add=True)
    # add methods to return winner and loser


class Score(models.Model):
    p1_points = models.PositiveSmallIntegerField(default=0)
    p2_points = models.PositiveSmallIntegerField(default=0)
    game = models.OneToOneField(
        Game,
        related_name='score',
        on_delete=models.CASCADE
    )
