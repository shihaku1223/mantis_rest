import rest_api
import requests
import urllib.parse

import json

rest_api_list = rest_api.get_api_list()

class Client:

    def __init__(self, url, token):
        self.url = url
        self.token = token
        self.headers = {'Authorization': self.token}

        for api_name in rest_api_list:
            print(api_name)
            impl = getattr(rest_api, '__{}_impl'.format(api_name))
            setattr(Client, api_name, impl)

    def request(self, url):
        r = requests.get(url, headers=self.headers)
        return r.text


def get_obj(api):
    def wrap(params):
        r = api(params)
        return json.loads(r)
    return wrap

if __name__ == '__main__':
    print(rest_api_list)

    client = Client('https://enosta.olympus.co.jp/mantis/ipf3/app/',
            'token')
    result = get_obj(client.get_issue)({ ':issue_id': '1234' })
    print(result)
