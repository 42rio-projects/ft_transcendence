import os
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from .models import User
from twilio.rest import Client


SERVICE_SID = os.environ["TWILIO_SERVICE_SID"]
ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]


def profile(request):
    if request.method == "GET":
        return render(request, "profile.html")


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, "Incorrect username or password")
            return render(request, "login.html",
                          {"username": username,
                           "password": password})

        django_login(request, user)
        messages.success(request, "You are now logged in")
        return redirect("main")

    if request.method == "GET":
        return render(request, "login.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        context = {
            "username": username,
            "password": password,
            "confirm_password": confirm_password
        }

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already in use")
            return render(request, "register.html", context)

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, "register.html", context)

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters")
            return render(request, "register.html", context)

        user = User.objects.create_user(username=username, password=password)
        user.save()

        messages.success(request, "You are now registered and can log in")
        return redirect("login")

    if request.method == "GET":
        return render(request, "register.html")


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
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already in use")
            elif len(username) < 3:
                messages.error(
                    request, "Username must be at least 3 characters")
            else:
                user.username = username

                messages.success(request, "Username changed successfully")

        if email != user.email:
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already in use")
            elif len(email) < 3:
                messages.error(request, "Email must be at least 3 characters")
            else:
                user.email = email
                user.email_verified = False

                messages.success(request, "Email changed successfully")

        user.save()

        return render(request, "edit_profile.html",
                      {"username": username,
                       "email": email})

    if request.method == "GET":
        return render(request, "edit_profile.html",
                      {"username": request.user.username,
                       "email": request.user.email})


def verify_email(request):
    if request.method == "GET":
        return render(request, "verify_email.html")


def receive_email_code(request):
    if request.method == "POST":
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
        return render(request, "verify_email.html",
                      {"code": code})
