from django.http import HttpResponse
from django.template import loader


def friendlist(request):
    template = loader.get_template("user/friendlist.html")
    context = {}
    return HttpResponse(template.render(context, request))


def friendInvites(request):
    template = loader.get_template("user/friend_invites.html")
    context = {}
    return HttpResponse(template.render(context, request))
