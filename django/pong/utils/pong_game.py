from pong.models import Game
from pong.models import Tournament
from django.contrib.auth.models import User


NO_GAMES = "Error: There are no records of games played."
NO_TOURNAMENT = "Error: This tournament does not exist: "
NO_TOURNAMENT_NAME = "Error: The tournament round field was set without a tournament name."
NO_TOURNAMENT_ROUND = "Error: The tournament field was set without a tournament round."
SAVE_FAIL = "Error: Failed to save game instance."
INTERNAL_ERROR = "Error: Server error ocurred."


def get_game_instances():
    try:
        return Game.objects.all().values()
    except Game.DoesNotExist as e:
        raise Game.DoesNotExist(NO_GAMES) from e
    except Exception as e:
        raise Exception(INTERNAL_ERROR) from e


def create_game(data):
    game = Game(winner_points=0, loser_points=0)
    if "tournament" in data and "tournament_round" in data:
        try:
            game.tournament = Tournament.objects.get(
                name=data["tournament"])
            game.tournament_round = data["tournament_round"]
        except Tournament.DoesNotExist as e:
            raise Tournament.DoesNotExist(
                NO_TOURNAMENT + data["tournament"]) from e
    elif "tournament" in data:
        raise Tournament.DoesNotExist(NO_TOURNAMENT_ROUND)
    elif "tournament_round" in data:
        raise Tournament.DoesNotExist(NO_TOURNAMENT_NAME)
    if "winner" in data:
        game.winner = User.objects.get(username=data["winner"])
    if "loser" in data:
        game.loser = User.objects.get(username=data["loser"])
    try:
        game.save()
    except Exception as e:
        raise Exception(SAVE_FAIL) from e
