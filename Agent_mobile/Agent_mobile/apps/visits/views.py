from django.shortcuts import render, redirect
from .models import Agent
from .models import Visit
from django import template

register = template.Library()


def index(request):
    agent = Agent.get_Agent(request)
    visit_list = Visit.objects.all().order_by('visitDate')
    return render(request, 'visits/main_visits.html', {'agent': agent, 'visits': visit_list})


@register.filter
def lookup(d, key):
    return d[key]
