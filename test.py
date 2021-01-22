from mantis_rest import rest_api
from mantis_rest.client import Client
from mantis_rest.client import get_obj

import json

rest_api_list = rest_api.get_api_list()


if __name__ == '__main__':
    print(rest_api_list)

    client = Client('https://enosta.olympus.co.jp/mantis/ipf3/app/',
            'token')
    obj = get_obj(client.get_issue)({ ':issue_id': '48365' })
    print(json.dumps(obj, indent=1))

    client.download_attachments(48361)
    #client.update_handler(48365, '10079186')

    """
    get_obj(client.get_issue_files)({ ':issue_id': '1234' })
    get_obj(client.get_all_issues)({ 'page_size': '50', 'page': '1' })
    get_obj(client.get_all_projects)()
    get_obj(client.get_filter)({ 'filter_id': '11092' })
    get_obj(client.user_info)()
    projects = get_obj(client.get_all_projects)().projects
    for p in projects:
        print(p.id, p.name, p.status.name, p.description)

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

    issue_obj = create_obj(client.create_issue)(data=data)
    print(issue_obj.issue.id)

    issue_obj = get_obj(client.get_issue)({ ':issue_id': '48361' })
    print(issue_obj.issues[0].summary)
    issue_obj.issues[0].summary = "This is a test issue summary updated"

    _data = {
        "summary": "This is a test issue summary updated updated",
    }
    updated_issue_obj = update_obj(client.update_issue)({
        ':issue_id': str(issue_obj.issues[0].id)
    }, data=_data)
    print(updated_issue_obj.issues[0].summary)

    #client.upload_attachments(48361, ['log2'])
    note = client.create_note(48361, 'test', ['log2'])
    print(note.note.id)

    obj = get_obj(client.get_all_issues)({
        'project_id': '208',
        'filter_id': '11092',
        'page_size': '50',
        'page': '2'
    })
    for issue in obj.issues:
        print(issue.id)
    print(len(obj.issues))
    """
