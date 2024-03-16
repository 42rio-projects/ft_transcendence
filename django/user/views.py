import os
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from .models import User
from twilio.rest import Client
from .forms import ChangePasswordForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, redirect
from django.core.exceptions import PermissionDenied

import user.models as models

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

@login_required
def upload_avatar(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'upload_avatar.html', {'form': form})


def change_password(request):
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        email_verified = request.user.email_verified
        if not email_verified:
            messages.error(request, "You must verify your email before changing your password")
            return render(request, "change_password.html", {"form": form})
        if form.is_valid():
            user = request.user
            current_password = form.cleaned_data.get("current_password")
            if (user.check_password(current_password)):
                new_password = form.cleaned_data.get("new_password")
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password changed successfully")
            else :
                form.add_error('current_password', "Senha atual incorreta")

    if request.method == 'GET':
        form = ChangePasswordForm()
    return render(request, "change_password.html", {"form": form})


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


def friends(request):
    template = loader.get_template('user/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def friendlist(request):
    template = loader.get_template("user/friendlist.html")
    context = {}
    return HttpResponse(template.render(context, request))


def friendInvitesSent(request):
    template = loader.get_template("user/invites_sent.html")
    context = {}
    return HttpResponse(template.render(context, request))


def friendInvitesReceived(request):
    template = loader.get_template("user/invites_received.html")
    context = {}
    return HttpResponse(template.render(context, request))


def sendFriendInvites(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        user = get_object_or_404(
            models.User,
            username=name,
        )
        try:
            request.user.add_friend(user)
            # add 201 response that is not rendered on the front end
        except Exception as e:
            return HttpResponse(e)
    template = loader.get_template("user/send_invites.html")
    context = {}
    return HttpResponse(template.render(context, request))


def excludeFriend(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(
            models.User,
            pk=user_id,
        )
        try:
            request.user.del_friend(user)
        except Exception as e:
            return HttpResponse(e)
    return redirect('friendList')


def respondFriendInvite(request, invite_id):
    invite = get_object_or_404(
        models.FriendInvite,
        pk=invite_id,
    )
    if invite.receiver != request.user:
        raise PermissionDenied
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'accept':
            invite.respond(accepted=True)
        elif action == 'reject':
            invite.respond(accepted=False)
        else:
            raise Exception('Invalid action')
    return redirect('friendInvitesReceived')


def cancelFriendInvite(request, invite_id):
    if request.method == 'POST':
        invite = get_object_or_404(
            models.FriendInvite,
            pk=invite_id,
        )
        if invite.sender != request.user:
            raise PermissionDenied
        invite.delete()
    return redirect('friendInvitesSent')
