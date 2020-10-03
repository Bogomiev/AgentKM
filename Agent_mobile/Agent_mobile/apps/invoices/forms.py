from django import forms
from django.contrib.admin.widgets import AdminTimeWidget
from django.utils.safestring import mark_safe
from .models import Invoice, InvoiceItem
from django.forms import widgets
from ..core.models import Agent


class InvoiceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(InvoiceForm, self).__init__(*args, **kwargs)

        if kwargs.__contains__('initial'):
            if not kwargs['initial']['enabled']:
                for field in self.fields:
                    self.fields[field].widget.attrs['disabled'] = 'disabled'

    def save(self, *args, **kwargs):
        return super(InvoiceForm, self).save(*args, **kwargs)

    class Meta:
        model = Invoice
        fields = ('date', 'price_type', 'promo', 'to_accounting')
        help_texts = {
            'date': '',
            'price_type': '',
            'promo': '',
            'to_accounting': '',
        }

        widgets = {
            'date': widgets.SelectDateWidget()
        }


class InvoiceItemForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(InvoiceItemForm, self).__init__(*args, **kwargs)

        if kwargs.__contains__('initial'):
            if not kwargs['initial']['enabled']:
                for field in self.fields:
                    self.fields[field].widget.attrs['disabled'] = 'disabled'

    def save(self, *args, **kwargs):
        return super(InvoiceItemForm, self).save(*args, **kwargs)

    class Meta:
        model = InvoiceItem
        fields = ('num', 'product', 'number', 'price', 'summ', 'discont')
        help_texts = {
            'product': '',
            'number': '',
            'price': '',
            'summ': '',
            'discont': '',
        }

        widgets = {

        }
