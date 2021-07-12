from .utils import *
from datetime import datetime

from ..api import API


def load_agents(api: API, base_url: str):
    agents = get_to_1c(f'{base_url}agents')['data']['agents']
    api.post('agent', {'data': agents})


def load_clients(api: API, base_url: str):
    clients = get_to_1c(f'{base_url}clients')['data']['clients']
    api.post('client', {'data': clients})


def load_shops(api: API, base_url: str):
    shops = get_to_1c(f'{base_url}shops')['data']['shops']
    api.post('shop', {'data': shops})


def start_exchange():
    print('============================================>>>>')
    print(f'Exchange start: {datetime.now()}')

    api = API()
    base_url = get_env_value("TRADE_URL")

    load_agents(api, base_url)
    load_clients(api, base_url)
    load_shops(api, base_url)

    print('<<<<============================================')
    print(f'Exchange finish: {datetime.now()}')


if __name__ == "__main__":
    start_exchange()