from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, redirect
from django.core.exceptions import PermissionDenied

import user.models as models


def friends(request):
    template = loader.get_template('user/friends.html')
    context = {}
    return HttpResponse(template.render(context, request))


def friendlist(request):
    template = loader.get_template("user/friendlist.html")
    context = {}
    return HttpResponse(template.render(context, request))


def friendInvites(request):
    template = loader.get_template("user/friend_invites.html")
    context = {}
    return HttpResponse(template.render(context, request))


def friendInvitesSent(request):
    template = loader.get_template("user/friend_invites_sent.html")
    context = {}
    return HttpResponse(template.render(context, request))


def friendInvitesReceived(request):
    template = loader.get_template("user/friend_invites_received.html")
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


def sendInvite(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        user = get_object_or_404(
            models.User,
            username=name,
        )
        try:
            request.user.add_friend(user)
        except Exception as e:
            return HttpResponse(e)
    return redirect('friendInvites')


def respondInvite(request, invite_id):
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
    return redirect('friendInvites')
