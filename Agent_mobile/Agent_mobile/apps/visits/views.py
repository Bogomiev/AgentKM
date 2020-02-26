from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context = {
        'agent': 'Агентик'
    }
    return render(request, 'visits/main_visits.html', context)