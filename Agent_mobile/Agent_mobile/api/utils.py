from django.http import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from annoying.functions import get_object_or_None


def get_api(request, model, serializer, name_guid, name_str, **kwargs):
    if kwargs.__contains__('guid'):
        _kwargs = {
            name_guid: kwargs[name_guid],
        }
        obj = get_object_or_None(model, **_kwargs)
        many = False
    else:
        obj = model.objects.all()
        many = True

    try:
        data = serializer(obj, many=many).data
        response = {'resultCode': 0, 'messages': [], 'data': data}
    except Exception as exc:
        response = {'resultCode': 1, 'messages': [f'{name_str} не определен: {exc}'], 'data': {}}

    return JsonResponse(response, safe=False)


def post_api(request, save_func, name_guid, name_api, **kwargs):
    try:
        data = JSONParser().parse(request)['data']
        response_data = {}
        if isinstance(data, list):
            for obj in data:
                response_data[obj[name_guid]] = save_func(obj)
        else:
            response_data[data[name_guid]] = save_func(data)

        response = {'resultCode': 0, 'messages': [], 'data': response_data}
    except Exception as exc:
        response = {'resultCode': 1, 'messages': [f'Ошибка api/{name_api}/post: {exc}'], 'data': {}}

    response_status = status.HTTP_201_CREATED if response['resultCode'] == 0 else status.HTTP_400_BAD_REQUEST

    return JsonResponse(response, status=response_status)
