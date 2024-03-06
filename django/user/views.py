from django.http import HttpResponse
from django.template import loader


def friendlist(request):
    template = loader.get_template("user/friendlist.html")
    context = {}
    return HttpResponse(template.render(context, request))
