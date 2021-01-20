import inspect
import requests
import sys
import re
import urllib.parse as urlparse
from urllib.parse import urlencode

from types import ModuleType

# issue API
get_issue = 'api/rest/issues/:issue_id'
get_issue_files = 'api/rest/issues/:issue_id/files'
get_issue_file = 'api/rest/issues/:issue_id/files/:file_id'

get_all_issues = 'api/rest/issues'
create_issue = 'api/rest/issues/'
update_issue = 'api/rest/issues/:issue_id'
add_attachments = 'api/rest/issues/:issue_id/files'

create_issue_note = 'api/rest/issues/:issue_id/notes'

# project API
get_all_projects = 'api/rest/projects'

# filter API
get_all_filters = 'api/rest/filters'
get_filter = 'api/rest/filters/:filter_id'
# delete_filter = 'api/rest/filters/:filter_id'

# user API
user_info = 'api/rest/users/me'

def get_api_list():
    rest_api_list = \
        [k for k, v in globals().items() \
          if not k.startswith('__') \
            and not callable(v) \
            and not isinstance(v, ModuleType) \
            and not isinstance(v, type)
        ]
    return rest_api_list

def get_api_path(co_name):

    """
    frames = inspect.getouterframes(inspect.currentframe())
    co_name = frames[1].frame.f_code.co_name[2:]
    s = len(co_name) - 5

    api_name = co_name[:s]
    print(sys.modules[__name__])
    """
    co_name = co_name[2:]
    s = len(co_name) - 5

    api_name = co_name[:s]
    return getattr(sys.modules[__name__], api_name)

def fill_api_path(path, params):
    if params is None:
        return path

    rep = dict((re.escape(k), v) for k, v in params.items())
    pattern = re.compile("|".join(rep.keys()))

    _path = pattern.sub(lambda m: rep[re.escape(m.group(0))], path)

    _params = {k: v for k, v in params.items() if k[0] != ':'}
    url_parts = list(urlparse.urlparse(_path))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(_params)

    url_parts[4] = urlencode(query)

    return urlparse.urlunparse(url_parts)

