import os
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from .models import User
from .validate import validate_username, validate_password, validate_confirm_password, validate_email
from twilio.rest import Client


SERVICE_SID = os.environ["TWILIO_SERVICE_SID"]
ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]


def profile(request):
    return render(request, "profile.html")


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            username=username, password=password)
        if user:
            django_login(request, user)
            return redirect("home")

        data = {
            "error": "Incorrect username or password",
            "username": username,
            "password": password
        }

    elif request.method == "GET":
        data = {
            "error": "",
            "username": "",
            "password": ""
        }

    return render(request, "login.html", data)


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        validate_username(request, username)
        validate_password(request, password)
        validate_confirm_password(
            request, password, confirm_password)

        if not messages.get_messages(request):
            user = User.objects.create_user(
                username=username, password=password)
            user.save()

            messages.success(request, "You are now registered and can log in")
            return redirect("login")

        data = {
            "username": username,
            "password": password,
            "confirm_password": confirm_password
        }

    elif request.method == "GET":
        data = {
            "username": "",
            "password": "",
            "confirm_password": ""
        }

    return render(request, "register.html", data)


def logout(request):
    if request.method == "GET":
        django_logout(request)
        messages.success(request, "You are now logged out")

    return render(request, "logout.html")


def edit_profile(request):
    if request.method == "POST":
        user = request.user

        username = request.POST.get("username")
        email = request.POST.get("email")

        if username != user.username:
            validate_username(request, username)

        if email != user.email:
            validate_email(request, email)

        if not messages.get_messages(request):
            if username != user.username:
                user.username = username
                messages.success(request, "Username updated")

            if email != user.email:
                user.email = email
                user.email_verified = False
                messages.success(request, "Email updated")

            user.save()

        data = {
            "username": username,
            "email": email
        }

    elif request.method == "GET":
        user = request.user

        data = {
            "username": user.username,
            "email": user.email
        }

    return render(request, "edit_profile.html", data)


def verify_email(request):
    return render(request, "verify_email.html")


def receive_email_code(request):
    if request.method == "GET":
        user = request.user

        verification = Client(ACCOUNT_SID, AUTH_TOKEN).verify.v2.services(
            SERVICE_SID).verifications.create(to=user.email, channel="email")

        status = verification.status

        if status == "pending":
            messages.success(request, "Verification code sent")
            return render(request, "verify_email.html")

        messages.error(request, f"Verification code {status}")

    return render(request, "verify_email.html")


def confirm_email_code(request):
    if request.method == "POST":
        user = request.user

        code = request.POST.get("code")

        verification = Client(ACCOUNT_SID, AUTH_TOKEN).verify.v2.services(
            SERVICE_SID).verification_checks.create(to=user.email, code=code)

        status = verification.status

        if status == "approved":
            user.email_verified = True
            user.save()

            messages.success(request, "Verification code approved")
            return redirect("profile")

        messages.error(request, f"Verification code {status}")

        data = {
            "code": code
        }

    elif request.method == "GET":
        data = {
            "code": ""
        }

    return render(request, "verify_email.html", data)
