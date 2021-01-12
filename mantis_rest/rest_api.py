import inspect
import requests
import urllib.parse
import sys
import re

from types import ModuleType

get_issue = 'api/rest/issues/:issue_id'

def get_api_list():
    rest_api_list = \
        [k for k, v in globals().items() \
          if not k.startswith('__') \
            and not callable(v) \
            and not isinstance(v, ModuleType) \
            and not isinstance(v, type)
        ]
    return rest_api_list

def get_api_path(client):
    frames = inspect.getouterframes(inspect.currentframe())
    co_name = frames[1].frame.f_code.co_name[2:]
    s = len(co_name) - 5

    api_name = co_name[:s]
    return getattr(sys.modules[__name__], api_name)

def fill_api_path(path, params):
    rep = dict((re.escape(k), v) for k, v in params.items())
    pattern = re.compile("|".join(rep.keys()))

    return pattern.sub(lambda m: rep[re.escape(m.group(0))], path)

def __get_issue_impl(client, data):
    path = fill_api_path(get_api_path(client), data)
    url = urllib.parse.urljoin(client.url, path)
    return client.request(url)
