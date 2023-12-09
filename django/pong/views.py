from django.shortcuts import render

def menu(request):
    return render(request, "menu/index.html")

def game(request):
    return render(request, "game/index.html")