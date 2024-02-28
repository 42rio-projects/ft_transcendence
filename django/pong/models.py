from django.db import models
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)


class Tournament(models.Model):
    name = models.CharField(max_length=100, unique=True)
    date = models.DateField(auto_now_add=True)
    players = models.ManyToManyField(User, related_name='tournaments')
    winner = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='championships'
    )

    def new_round(self):
        if self.players.count() < 4:
            raise Exception('Not enough players in the tournament.')
        elif self.rounds.count() == 0:
            round = Round(tournament=self, number=1)
            round.save()
            round.first_games(self.players.iterator())


class Round(models.Model):
    tournament = models.ForeignKey(
        Tournament,
        related_name='rounds',
        on_delete=models.CASCADE
    )
    number = models.PositiveSmallIntegerField()

    def first_games(self, players):
        logger.warning('First round creation, players:')
        pair = []
        for player in players:
            pair.append(player)
            if len(pair) == 2:
                Game(player_1=pair[0], player_2=pair[1], round=self).save()
                pair.clear()
        if len(pair) == 1:
            Game(player_1=pair[0], round=self).save()

    def next_games(self, previous):
        logger.warning('Sequential round creation')


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
        on_delete=models.CASCADE,
        related_name='games'
    )
    date = models.DateField(auto_now_add=True)

    # Placeholder method to return winner
    def winner(self):
        return self.player_1

    # Placeholder method to return loser
    def loser(self):
        return self.player_2


class Score(models.Model):
    p1_points = models.PositiveSmallIntegerField(default=0)
    p2_points = models.PositiveSmallIntegerField(default=0)
    game = models.OneToOneField(
        Game,
        related_name='score',
        on_delete=models.CASCADE
    )
