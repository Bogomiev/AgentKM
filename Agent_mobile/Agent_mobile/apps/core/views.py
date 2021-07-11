from django.shortcuts import render, redirect
from ..core.models import Agent, ProductTree, Product
from django.http import JsonResponse, HttpResponse
import json
from django.core import serializers


def load_products():

    objs_json = list(ProductTree.objects.all().values('id', 'name', 'parent_id')).__str__()
    objs_json = objs_json.replace("'name':", "\"text\":")
    objs_json = objs_json.replace("'parent_id':", "\"parent\":")
    objs_json = objs_json.replace("'id':", "\"id\":")
    objs_json = objs_json.replace("<QuerySet ", "")
    objs_json = objs_json.replace("}]>", "}]")
    objs_json = objs_json.replace(": '", ": \"")
    objs_json = objs_json.replace("',", "\",")
    objs_json = objs_json.replace("'}]", "'}]")
    objs_json = objs_json.replace(": None", ": \"#\"")

    return objs_json


def items(request):
    response = HttpResponse(content=load_products())
    response['Content-Type'] = 'application/json'

    return response
