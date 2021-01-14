import inspect
import requests
import urllib.parse
import sys
import re

from types import ModuleType

# issue API
get_issue = 'api/rest/issues/:issue_id'
get_issue_files = 'api/rest/issues/:issue_id/files'
get_issue_file = 'api/rest/issues/:issue_id/files/:file_id'
get_all_issues = 'api/rest/issues?page_size=:page_size&page=:page'
get_issues_project = 'api/rest/issues?project_id=:project_id'
create_issue = 'api/rest/issues/'
update_issue = 'api/rest/issues/:issue_id'

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

    return pattern.sub(lambda m: rep[re.escape(m.group(0))], path)
