from django.contrib import messages
from .models import User


MIN_USERNAME_LENGTH = 2
MAX_USERNAME_LENGTH = 15
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 50


def validate_username(request, username):
    if User.objects.filter(username=username).exists():
        messages.error(request, "Username already in use")

    if len(username) < MIN_USERNAME_LENGTH:
        messages.error(
            request,
            f"Username must be at least {MIN_USERNAME_LENGTH} characters")

    if len(username) > MAX_USERNAME_LENGTH:
        messages.error(
            request,
            f"Username must be at most {MAX_USERNAME_LENGTH} characters")


def validate_password(request, password):
    if len(password) < MIN_PASSWORD_LENGTH:
        messages.error(
            request,
            f"Password must be at least {MIN_PASSWORD_LENGTH} characters")

    if len(password) > MAX_PASSWORD_LENGTH:
        messages.error(
            request,
            f"Password must be at most {MAX_PASSWORD_LENGTH} characters")


def validate_confirm_password(request, password, confirm_password):
    if password != confirm_password:
        messages.error(request, "Passwords do not match")


def validate_email(request, email):
    if User.objects.filter(email=email).exists():
        messages.error(request, "Email already in use")
