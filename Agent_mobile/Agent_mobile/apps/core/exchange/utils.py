import ast
import base64
import json
import requests

from ..utils import get_env_value


def trade_1c_headers():
    l_p = f'{get_env_value("TRADE_LOGIN")}:{get_env_value("TRADE_PASS")}'
    l_p_bytes = l_p.encode('ascii')
    base64_bytes = base64.b64encode(l_p_bytes)
    base64_l_p = base64_bytes.decode('ascii')
    return {'Authorization': f'Basic {base64_l_p}',
            'Content-Type': 'application/json'}


TRADE_1C_HEADERS = trade_1c_headers()


def get_to_1c(url):
    try:
        r = requests.get(url, headers=TRADE_1C_HEADERS)
        r.encoding = 'utf-8'
        content = json.loads(r.text)
    except Exception as e:
        return {'resultCode': 1,
                'messages': [f'недоступен сервер 1с {str(e)}'],
                'data': {}}

    return {'resultCode': content['resultCode'],
            'messages': content['messages'],
            'data': content['data']}


async def post_to_1c(url: str, data):
    try:
        r = requests.post(url, headers=TRADE_1C_HEADERS, data=data)
        r.encoding = 'utf-8'
        return ast.literal_eval(r.text)
    except Exception as e:
        return {'resultCode': 1,
                'messages': [f'недоступен сервер 1с {str(e)}'],
                'data': {}}
