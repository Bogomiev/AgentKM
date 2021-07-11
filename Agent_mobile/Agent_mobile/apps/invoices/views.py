from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from ..core.models import Agent
from .models import Invoice, InvoiceItem
from django import template
from .forms import InvoiceForm, InvoiceItemForm
from ..visits.models import Visit
from ..core.models import ProductTree
from ...utilities import split_date_time
from django.http import JsonResponse, HttpResponse
import uuid


def invoice_list_view(request):
    agent = Agent.get_Agent(request)
    invoice_list = Invoice.objects.filter(agent=agent['ref']).order_by('-date', )
    return render(request, 'invoices/invoices.html', {'agent': agent, 'invoice_list': invoice_list})


def invoice(request, id, form_owner='invoice'):
    agent = Agent.get_Agent(request)
    _invoice = Invoice.objects.select_related("visit").get(id=id)
    enabled = agent['id'] != 0 and _invoice.status != 2
    visit = _invoice.visit
    items = InvoiceItem.objects.filter(ref=_invoice).order_by('num')

    if request.method == "POST":
        if not enabled:
            return redirect('/' + form_owner)

        form = InvoiceForm(request.POST, instance=_invoice)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()

            return redirect('/' + form_owner)
    else:
        form = InvoiceForm(instance=_invoice,
                           initial={'agent_id': agent['id'],
                                    'enabled': enabled})

    return render(request, 'invoices/invoice.html',
                  {'form': form,
                   'invoice_id': _invoice.id,
                   'agent': agent,
                   'visit': visit,
                   'items': items,
                   'form_owner': form_owner,
                   'status': _invoice.status,
                   'enabled': enabled,
                   'choice_product': False})


def save_invoice(invoice, visit, guid, status):
    _guid = uuid.uuid4().hex if guid is None else guid

    invs = Invoice.objects.filter(guid=guid)
    if not invs.exists():
        _invoice = Invoice.objects.create(guid=guid,
                                          visit=visit,
                                          date=timezone.localtime(timezone.now()),
                                          agent=visit.agent,
                                          client=visit.shop.client,
                                          shop=visit.shop,
                                          marked=False) \
            if invoice is None else invoice
    else:
        _invoice = invs[0]

    if _invoice.visit != visit:
        _invoice.visit = visit
        _invoice.agent = visit.agent
        _invoice.client = visit.shop.client
        _invoice.shop = visit.shop

    _invoice.marked = False
    _invoice.status = status
    _invoice.save()

    return _invoice


def invoice_new(request, visit_id, form_owner='invoice'):
    agent = Agent.get_Agent(request)
    visit = Visit.objects.select_related("shop").get(id=visit_id)
    enabled = agent['id'] != 0

    if request.method == "POST":
        form = InvoiceForm(request.POST)
        if form.is_valid():
            _invoice = form.save(commit=False)
            save_invoice(_invoice, visit, None, 1)

            return redirect('/' + form_owner)
    else:
        form = InvoiceForm(
            initial={'date': timezone.localtime(timezone.now()),
                     'agent_id': agent['id'],
                     'enabled': enabled})

    return render(request, 'invoices/invoice.html',
                  {'form': form,
                   'invoice_id': 0,
                   'agent': agent,
                   'visit': visit,
                   'items': [],
                   'form_owner': form_owner,
                   'status': 0,
                   'enabled': enabled,
                   'choice_product': False})


def item_new(request, invoice_id: int, visit_id):
    agent = Agent.get_Agent(request)
    agent_id = agent['id']
    enabled = agent_id != 0
    visit = Visit.objects.select_related("shop").get(id=visit_id)
    print("invoice_id: ", invoice_id)
    if invoice_id == "0":
        _guid = f'{(agent_id.__str__() + "x")[:8]}-GUID-XXXX-XXXX-XXXXXXXXXXXX'
        _invoice = save_invoice(None, visit, _guid, 1)
    else:
        _invoice = Invoice.objects.get(id=invoice_id)
    items = InvoiceItem.objects.filter(ref=_invoice).order_by('num')

    if request.method == "POST":
        form = InvoiceItemForm(request.POST)
        if form.is_valid():
            _invoice_item = form.save(commit=False)
            _invoice_item.ref = _invoice
            if items.count > 0:
                num = items[items.count - 1].num + 1
            else:
                num = 1
            _invoice_item.num = num
            _invoice_item.save()

            return redirect('/')
    else:
        form = InvoiceItemForm(
            initial={'date': timezone.localtime(timezone.now()),
                     'agent_id': agent['id'],
                     'enabled': enabled})

    return render(request, 'invoices/item.html',
                  {'form': form,
                   'agent': agent,
                   'enabled': enabled})
