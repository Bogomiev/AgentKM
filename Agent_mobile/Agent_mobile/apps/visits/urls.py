from django.conf.urls import url
from django.urls import path
from django.views.generic import ListView, DetailView
from . import views
from .models import Visit

urlpatterns = [
    path('new/', views.visit_new, name='visit_new'),
    path('<int:id>/', views.visit, name='visit'),
    # url(r'^add/$', views.visit, name='visit'),
    # url(r'^(?P<pk>\d+)$', DetailView.as_view(model=Visit, template_name="visits/visit.html")),
    url(r'^$', views.visit_list_view, name='visit_list_view'),
]