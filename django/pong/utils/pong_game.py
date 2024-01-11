from pong.models import Game
from pong.models import Tournament
from django.contrib.auth.models import User


NO_GAMES = "There are no records of games played."
NO_TOURNAMENT = "Error: No tournament exists named: "
NO_TOURNAMENT_NAME = "Error: The tournament round field was set without a tournament name."
NO_TOURNAMENT_ROUND = "Error: The tournament field was set without a tournament round."
NO_ID = "Error: No game id was supplied in the request"
DOESNT_EXIST = "Error: Game does not exist"
SAVE_FAIL = "Error: Failed to save game instance."
INTERNAL_ERROR = "Error: Server error ocurred."


def get_game_instances():
    try:
        games = Game.objects.all().values()
        if not games:
            return NO_GAMES
        return games
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


def delete_game(data):
    if "id" not in data:
        raise KeyError(NO_ID)
    try:
        game = Game.objects.get(id=data["id"])
        game.delete()
    except Game.DoesNotExist as e:
        raise Game.DoesNotExist(DOESNT_EXIST) from e
    except Exception as e:
        raise Exception(INTERNAL_ERROR) from e
