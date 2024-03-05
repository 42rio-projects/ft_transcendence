import os
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from user.models import User
from django.contrib.auth.decorators import login_required
from twilio.rest import Client

# Create your views here.


SERVICE_SID = os.environ["TWILIO_SERVICE_SID"]
ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]


def login(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if not user:
            messages.error(request, "Invalid credentials")
            return redirect("login")

        django_login(request, user)

        messages.success(request, "You are now logged in")
        return redirect("index")

    if request.method == "GET":
        return render(request, "login.html")


def register(request):
    if request.user.is_authenticated:
        return redirect("welcome.html")

    if request.method == "POST":
        username = request.POST["username"]

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already in use")
            return redirect("register")

        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters")
            return redirect("register")

        user = User.objects.create_user(username=username, password=password)
        user.save()

        messages.success(request, "You are now registered and can log in")
        return redirect("login")

    if request.method == "GET":
        return render(request, "register.html")


def logout(request):
    django_logout(request)
    return render(request, "logout.html")


@login_required(login_url="login")
def receive_code(request):
    if request.method == "POST":
        to = request.POST["to"]
        if not to:
            messages.error(request, "Email is required")
            return redirect("receive_code")

        channel = "email"

        verification = Client(ACCOUNT_SID, AUTH_TOKEN).verify.v2.services(
            SERVICE_SID).verifications.create(to=to, channel=channel)

        status = verification.status

        if status == "pending":
            messages.success(request, "Verification code sent")
            return redirect("confirm_code")
        else:
            messages.error(request, f"Verification code {status}")
            return redirect("receive_code")

    if request.method == "GET":
        return render(request, "receive_code.html")


@login_required(login_url="login")
def confirm_code(request):
    if request.method == "POST":
        to = request.POST["to"]
        if not to:
            messages.error(request, "Email is required")
            return redirect("confirm_code")

        code = request.POST["code"]
        if code:
            verification = Client(ACCOUNT_SID, AUTH_TOKEN).verify.v2.services(
                SERVICE_SID).verification_checks.create(to=to, code=code)
        else:
            messages.error(request, "Code is required")
            return redirect("confirm_code")

        status = verification.status

        if status == "approved":
            messages.success(request, "Verification code approved")
            return redirect("index")
        else:
            messages.error(request, f"Verification code {status}")
            return redirect("confirm_code")

    if request.method == "GET":
        return render(request, "confirm_code.html")
