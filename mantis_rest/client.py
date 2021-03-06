from mantis_rest import rest_api
import requests
import urllib.parse

import json
import base64
from pathlib import Path

rest_api_list = rest_api.get_api_list()

class ObjectDict(dict):
    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)

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

        setattr(impl, '__client', self)
        impl.__name__ = name
        return impl

    def request(self, url, method='GET', data=None, headers=None):
        if headers is None:
            headers = self.headers
        else:
            headers = {**self.headers, **headers}

        r = requests.request(method, url, headers=headers, data=data)
        r.raise_for_status()

        return r.text

    def create_note(self, issue_id, text, file_paths=[]):

        data = {
            "text": text,
        }

        if file_paths is not None:
            data["files"] = []
        for path in file_paths:
            p = Path(path)
            data["files"].append({
              "name": p.name,
              "content": file2base64(path)
            })

        note = create_obj(self.create_issue_note)(
            { ':issue_id': str(issue_id) },
            data=data)

        return note

    def update_handler(self, issue_id, handler_name):

        _data = {
            "handler": {
                "name": handler_name
            }
        }
        updated_issue_obj = update_obj(self.update_issue)({
            ':issue_id': str(issue_id)
        }, data=_data)
        return updated_issue_obj

    def upload_attachments(self, issue_id, file_paths):
        files = []

        for path in file_paths:
            p = Path(path)
            files.append({
              "name": p.name,
              "content": file2base64(path)
            })

        data = { "files": files }

        # No object will be returned
        create_obj(self.add_attachments)(
            { ':issue_id': str(issue_id) },
            data=data)

    def download_attachment(self, issue_id, attachment_id, dest='.'):

        _obj = get_obj(self.get_issue_file)(
            { ':issue_id': str(issue_id), ':file_id': str(attachment_id) })

        print('download {} to {}'.format(attachment_id, dest))

        Path('{}'.format("{}".format(dest))).mkdir(parents=True, exist_ok=True)
        file_content = base64.b64decode(_obj.files[0].content)
        with open("{}/{}".format(dest,
            _obj.files[0].filename), "wb") as f:
            f.write(file_content)

    def download_attachments(self, issue_id, dest='.'):

        issue_obj = get_obj(self.get_issue)({ ':issue_id': str(issue_id) })
        for attachment in issue_obj.issues[0].attachments:
            print('download ', attachment.id, attachment.filename)

            _obj = get_obj(self.get_issue_file)(
                { ':issue_id': str(issue_id), ':file_id': str(attachment.id) })

            Path('{}'.format("{}/{}".format(dest, attachment.id))).mkdir(parents=True, exist_ok=True)
            file_content = base64.b64decode(_obj.files[0].content)
            with open("{}/{}/{}".format(dest,
                attachment.id,
                _obj.files[0].filename), "wb") as f:
                f.write(file_content)

def get_obj(api):
    def wrap(params=None):
        path = rest_api.fill_api_path(
                    rest_api.get_api_path(api.__name__), params)

        url = urllib.parse.urljoin(api.__client.url, path)
        r = api.__client.request(url)

        if r is None or r == "":
            return None
        return json.loads(r, object_hook=ObjectDict)
    return wrap

def create_obj(api):
    def wrap(params=None, data=None):
        path = rest_api.fill_api_path(
                    rest_api.get_api_path(api.__name__), params)

        url = urllib.parse.urljoin(api.__client.url, path)

        h = { 'Content-Type': 'application/json' }
        data = json.dumps(data)
        r = api.__client.request(url, method='POST', headers=h, data=data)

        if r is None or r == "":
            return None
        return json.loads(r, object_hook=ObjectDict)
    return wrap

def update_obj(api):
    def wrap(params=None, data=None):
        path = rest_api.fill_api_path(
                    rest_api.get_api_path(api.__name__), params)
        url = urllib.parse.urljoin(api.__client.url, path)

        h = { 'Content-Type': 'application/json' }
        r = api.__client.request(url, method='PATCH',
                headers=h,
                data=json.dumps(data))

        if r is None or r == "":
            return None
        return json.loads(r, object_hook=ObjectDict)
    return wrap

def file2base64(filePath):
    base64String = None
    with open(filePath, 'rb') as f:
        binary = f.read()
        base64String = base64.b64encode(binary).decode()
    return base64String

def get_custom_field(issue, field_name):
    return [field for field in issue.custom_fields if field['field']['name'] == field_name]

