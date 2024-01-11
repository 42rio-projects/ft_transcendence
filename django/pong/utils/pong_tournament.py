from pong.models import Tournament
from django.db import IntegrityError

NO_TOURNAMENTS = "There are no records of tournaments played."
NO_NAME = "Error: No tournament name was supplied in the request"
DUPLICATE = "Error: Tournament name already used."
DOESNT_EXIST = "Error: Tournament does not exist"
INTERNAL_ERROR = "Error: Server error ocurred."


def get_tournaments():
    try:
        tournaments = Tournament.objects.all().values()
        if not tournaments:
            return NO_TOURNAMENTS
        return tournaments
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


def delete_tournament(data):
    if "name" not in data:
        raise KeyError(NO_NAME)
    try:
        tournament = Tournament.objects.get(name=data["name"])
        tournament.delete()
    except Tournament.DoesNotExist as e:
        raise Tournament.DoesNotExist(DOESNT_EXIST) from e
    except Exception as e:
        raise Exception(INTERNAL_ERROR) from e
