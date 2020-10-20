import requests
import traceback


class ServerRequest(object):

    def __init__(self, host):
        self.host = host
        self.token = None

    def get_token(self):
        return self._request('login', 'post', {
            'code': 'mncu2jhhhhusdgfsdfsdflkj87',
            'name': 'mncu',
            'user_avatar': ''
        }, False)['token']

    def _request(self, suffix_url, method, params, need_token=True):
        url = self.host + suffix_url
        if need_token and self.token is None:
            self.token = self.get_token()
        headers = {
            'F-TOKEN': self.token
        }

        if method == 'get':
            r = requests.request(method, url, params=params, headers=headers)
        else:
            r = requests.request(method, url, json=params, headers=headers)

        try:
            print(r.content)
            if r.status_code == 200:
                r = r.json()
        except Exception:
            traceback.print_exc()
            raise Exception('数据格式非json')
        if r['code'] != 0:
            raise Exception(r['msg'])
        else:
            return r['data']

    def create_activity(self, name, end_time=None):
        self._request('activity', 'post', {
            'name': name,
            'end_time': end_time or 1568044800
        })

    def get_activity_detail(self, activity_id):
        self._request('activity', 'get', {'id': activity_id})


local_server = ServerRequest('http://127.0.0.1:5000/app/')

local_server.get_activity_detail(1)
