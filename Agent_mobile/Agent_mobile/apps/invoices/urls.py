from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^new/(?P<visit_id>[0-9]+)/(?P<form_owner>[\w\-]+)/$', views.invoice_new, name='invoice_new'),
    # url(r'^(?P<id>[0-9]+)/(?P<form_owner>\w+)/(?P<tree_id>[0-9]+)/$', views.invoice, name='invoice'),
    url(r'^(?P<id>[0-9]+)/(?P<form_owner>\w+)/$', views.invoice, name='invoice'),
    url(r'^$', views.invoice_list_view, name='invoice_list_view'),
    url(r'^item/new/(?P<invoice_id>[0-9]+)/(?P<visit_id>[0-9]+)/$', views.item_new, name='item_new'),
]