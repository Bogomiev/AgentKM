from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import auth

def index(request):
    context = {
        'agent': auth.get_user(request).username
    }
    return render(request, 'visits/main_visits.html', context)