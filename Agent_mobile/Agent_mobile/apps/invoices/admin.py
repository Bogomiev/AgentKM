from django.contrib import admin
from .models import Invoice
from .models import InvoiceItem

admin.site.register(Invoice)
admin.site.register(InvoiceItem)