from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Agent
from ..main_menu.models import Client
from .models import Visit
from django import template
from .forms import VisitForm
from ..main_menu.models import AgentShop
from ..main_menu.models import Shop
from ...utilities import split_date_time
from django.http import JsonResponse, HttpResponse

register = template.Library()


def visit_list_view(request):
    agent = Agent.get_Agent(request)
    visit_list = Visit.objects.filter(agent=agent['ref']).order_by('-visitDate', )
    return render(request, 'visits/main_visits.html', {'agent': agent, 'visit_list': visit_list})


def visit(request, id):
    agent = Agent.get_Agent(request)
    _visit = get_object_or_404(Visit, id=id)
    if request.method == "POST":
        form = VisitForm(request.POST, instance=_visit)

        if form.is_valid():
            post = form.save(commit=False)
            post.visitDate = split_date_time(post.visitDate, form.cleaned_data['visitTime'])
            post.save()
            return redirect('/visit')
            # return redirect('visits/main_visits.html', id=_visit.id)
    else:
        form = VisitForm(instance=_visit, initial={'visitTime': timezone.localtime(_visit.visitDate).time(),
                                                   'agent_id': agent['id']})

    return render(request, 'visits/visit.html', {'form': form, 'agent': agent})


def visit_new(request):
    agent = Agent.get_Agent(request)
    if request.method == "POST":
        form = VisitForm(request.POST)
        if form.is_valid():
            _visit = form.save(commit=False)
            _visit.agent = agent['ref']
            _visit.visitDate = split_date_time(_visit.visitDate, form.cleaned_data['visitTime'])
            _visit.marked = False
            _visit.save()
            return redirect('/visit')
    else:
        form = VisitForm(
            initial={'visitDate': timezone.localtime(timezone.now()), 'visitTime': timezone.localtime(timezone.now()),
                     'agent_id': agent['id']})

    return render(request, 'visits/visit.html', {'form': form, 'agent': agent})


def agent_shops(request):
    agent = Agent.get_Agent(request)['ref']
    available_shops_id = AgentShop.objects.filter(agent=agent).values_list('shop_id')
    clients = Client.objects.all()
    client_list = []
    letter = request.GET['filter']

    if letter != '...':
        for client in clients:
            if client.name[0].lower() == letter:
                client_list.append(client)
    else:
        client_list = clients

    shops = Shop.objects.filter(client__in=client_list, id__in=available_shops_id).order_by('name')
    shop_list = [{'value': 0, 'name': '---------'}]

    for shop in shops:
        shop_list.append({'value': shop.id, 'name': shop.__str__()})

    return JsonResponse({'shops': shop_list})
