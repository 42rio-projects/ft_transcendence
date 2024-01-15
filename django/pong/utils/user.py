from django.contrib.auth.models import User
from django.db import IntegrityError

NO_USERS = "There are no users on the database."
NO_USERNAME = "Error: No username was supplied."
NO_PASSWORD = "Error: No password was supplied."
FORBIDDEN = "Error: Insuficient permissions."
DUPLICATE = "Error: Username already in use"
DOESNT_EXIST = "Error: This user does not exist"
INTERNAL_ERROR = "Error: Server error ocurred."


def get_users():
    try:
        users = User.objects.all().values()
        if not users:
            return NO_USERS
        return users
    except Exception as e:
        raise Exception(INTERNAL_ERROR) from e


def create_user(data):
    if "username" not in data:
        raise KeyError(NO_USERNAME)
    elif "password" not in data:
        raise KeyError(NO_PASSWORD)
    try:
        user = User(username=data["username"], password=data["password"])
        user.save()
    except IntegrityError as e:
        raise IntegrityError(DUPLICATE) from e
    except Exception as e:
        raise Exception(INTERNAL_ERROR) from e


def delete_user(data):
    if "username" not in data:
        raise KeyError(NO_USERNAME)
    elif "password" not in data:
        raise KeyError(NO_PASSWORD)
    try:
        user = User.objects.get(username=data["username"])
        if user.password != data["password"]:
            raise IntegrityError
        user.delete()
    except IntegrityError:
        raise IntegrityError(FORBIDDEN)
    except User.DoesNotExist as e:
        raise User.DoesNotExist(DOESNT_EXIST) from e
    except Exception as e:
        raise Exception(INTERNAL_ERROR) from e
