import ast
import json
import requests
from .utils import get_env_value


class API:
    _access_token = ''
    _base_url = f'{get_env_value("API_URL")}{get_env_value("API_VERSION")}/'
    _user = get_env_value("API_USER")
    _password = get_env_value("API_PASSWORD")

    def _get_access_token(self) -> str:
        return self._access_token

    def _generate_access_token(self):
        headers = {'Content-Type': 'application/json'}
        data = {'username': self._user,
                'password': self._password}

        data_j = json.dumps(data)
        r = requests.post(f'{get_env_value("API_URL")}auth/jwt/create', headers=headers, json=json.loads(data_j))
        token_data = ast.literal_eval(r.text)
        self._access_token = token_data['access']

    def header(self):
        return {'Authorization': f'JWT {self._get_access_token()}',
                'Content-Type': 'application/json'}

    def _run_method(self, method: str, url: str, data):
        if method == 'GET':
            return requests.get(f'{self._base_url}{url}', headers=self.header())
        else:
            r = json.dumps(data)
            loaded_r = json.loads(r)
            return requests.post(f'{self._base_url}{url}', headers=self.header(), json=loaded_r)

    def _fetch(self, method: str, url: str, data):
        r = self._run_method(method, url, data)

        if r.status_code == 401:
            self._generate_access_token()
            r = self._run_method(method, url, data)

        r.encoding = 'utf-8'
        return r

    def get(self, url: str):
        try:
            r = self._fetch('GET', url, None)
            content = json.loads(r.text)
        except Exception as e:
            return {'resultCode': 1,
                    'messages': [f'Ошибка в методе get.{url}: {str(e)}'],
                    'data': {}}

        return {'resultCode': content['resultCode'],
                'messages': content['messages'],
                'data': content['data']}

    def post(self, url: str, data):
        try:
            r = self._fetch('POST', url, data)
            return ast.literal_eval(r.text)
        except Exception as e:
            return {'resultCode': 1,
                    'messages': [f'Ошибка в методе post.{url}: {str(e)}'],
                    'data': {}}
