import rest_api
import requests
import urllib.parse

import json

rest_api_list = rest_api.get_api_list()

class obj:
    def __init__(self, dict1):
        self.__dict__.update(dict1)

class Client:

    def __init__(self, url, token):
        self.url = url
        self.token = token
        self.headers = {'Authorization': self.token}

        for api_name in rest_api_list:

            impl_name = '__{}_impl'.format(api_name)
            try:
                impl = getattr(rest_api, impl_name)
                setattr(Client, api_name, impl)
            except AttributeError:
                impl = self.generate_api_impl(impl_name)
                setattr(Client, api_name, impl)

    def generate_api_impl(self, name):

        # default api implementation
        def impl(client, data):
            pass

        impl.__name__ = name
        return impl

    def request(self, url, data=None, headers=None):
        if headers is None:
            headers = self.headers
        else:
            headers = {**self.headers, **headers}

        if data is None:
            r = requests.get(url, headers=headers)
        else:
            print(url, data, headers)
            r = requests.post(url, headers=headers, data=data)

        return r.text

def get_obj(api):
    def wrap(params=None):
        path = rest_api.fill_api_path(
                    rest_api.get_api_path(api.__name__), params)

        url = urllib.parse.urljoin(client.url, path)
        r = client.request(url)

        if r is None or r == "":
            return None
        return json.loads(r, object_hook=obj)
    return wrap

def create_obj(api):
    def wrap(params=None):
        path = rest_api.fill_api_path(
                    rest_api.get_api_path(api.__name__), params)

        url = urllib.parse.urljoin(client.url, path)

        h = { 'Content-Type': 'application/json' }
        data = json.dumps(params)
        r = client.request(url, headers=h, data=data)

        if r is None or r == "":
            return None
        return json.loads(r, object_hook=obj)
    return wrap

if __name__ == '__main__':
    print(rest_api_list)

    client = Client('https://enosta.olympus.co.jp/mantis/ipf3/app/',
            'token')
    """
    get_obj(client.get_issue)({ ':issue_id': '1234' })
    get_obj(client.get_issue_files)({ ':issue_id': '1234' })
    get_obj(client.get_all_issues)({ ':page_size': '50', ':page': '1' })
    get_obj(client.get_issues_project)({ ':project_id': '1' })
    get_obj(client.get_all_projects)()
    get_obj(client.get_filter)({ ':filter_id': '11092' })
    get_obj(client.user_info)()
    projects = get_obj(client.get_all_projects)().projects
    for p in projects:
        print(p.id, p.name, p.status.name, p.description)
    """

    data = {
        "summary": "This is a test issue",
        "description": "This is a test description",
        "category": {
            "name": "General"
        },
        "project": {
            "name": "TEST"
        }
    }

    issue_obj = create_obj(client.create_issue)(data)
    print(issue_obj.issue.id)
