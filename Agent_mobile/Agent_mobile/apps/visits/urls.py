from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.visit_new, name='visit_new'),
    path('<int:id>/', views.visit, name='visit'),
    url(r'agent_shops/', views.agent_shops, name='agent_shops'),
    url(r'^$', views.visit_list_view, name='visit_list_view'),
]