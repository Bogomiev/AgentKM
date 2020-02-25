from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context = {
        'agent': 'Агентик'
    }
    return render(request, 'main_menu/homePage.html', context)
