from pong.models import Tournament
from django.db import IntegrityError

NO_TOURNAMENTS = "There are no records of tournaments played."
NO_NAME = "Error: No name was supplied to the tournament."
DUPLICATE = "Error: Tournament name already used."
INTERNAL_ERROR = "Error: Server error ocurred."


def get_tournaments():
    try:
        return Tournament.objects.all().values()
    except Tournament.DoesNotExist as e:
        raise Tournament.DoesNotExist(NO_TOURNAMENTS) from e
    except Exception as e:
        raise Exception(INTERNAL_ERROR) from e


def create_tournament(data):
    if "name" not in data:
        raise KeyError(NO_NAME)
    tournament = Tournament(name=data["name"])
    try:
        tournament.save()
    except IntegrityError as e:
        raise IntegrityError(DUPLICATE) from e
    except Exception as e:
        raise Exception(INTERNAL_ERROR) from e
