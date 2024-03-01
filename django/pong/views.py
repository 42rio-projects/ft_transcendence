from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url="login")
def index(request):
    context = {
        "username": request.user.username
    }

    return render(request, "index.html", context)
