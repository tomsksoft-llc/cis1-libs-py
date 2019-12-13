##############################################################################
#
# Copyright (c) 2019 TomskSoft LLC
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# FILE: redmine.py
# Authors: Dmitriy Tsvedel
#
##############################################################################
'''This is a script for update status of a issue your project in Redmine.
Optional, you can specify a note.

'''

import os
import sys
import json
import argparse
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


def get_status_identifier_by_name(status_name):
    req = Request('%s/issue_statuses.json' % redmine_host_project)
    req.add_header('X-Redmine-API-Key', redmine_access_key)
    try:
        content = urlopen(req).read()
    except URLError as e:
        print('We failed to reach a server.')
        print('Reason: ', e.reason)
        return
    else:
        data = json.loads(content)
    try:
        return list(filter(lambda x: x['name'].upper() == status_name.upper(), data['issue_statuses']))[0]['id']
    except IndexError:
        print("The issue status '%s' does not exist." % status_name)


def update_status_issue(issue, status_id, notes):
    values = '''{ "issue": { "status_id": "%s", "notes": "%s" } }''' % (status_id, notes)
    req = Request('%s/issues/%s.json' % (redmine_host_project, issue), data=values.encode(), method='PUT')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Redmine-API-Key', redmine_access_key)
    try:
        with urlopen(req) as f:
            pass
    except HTTPError as e:
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', e.code)
        return e.code
    except URLError as e:
        print('We failed to reach a server.')
        print('Reason: ', e.reason)
        return e.code
    else:
        return f.code


def use_as_os_command():
    ''' redmine.py <issue> <status> [notes]

    issue - A hash of the issue is bound to a project.
    status - Status workflow. Issues reports should show only statuses used by the project
    notes - Comments about the update

    Return value:
       0 - on success
       non zero - if any error
    '''

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-h', '--help', action='store_true')
    parser.add_argument("issue", nargs="?")
    parser.add_argument("status", nargs="?")
    parser.add_argument("notes", nargs='?', default='')
    parser.usage = use_as_os_command.__doc__

    args = parser.parse_args()

    if args.help:
        print('usage: ' + use_as_os_command.__doc__)
        sys.exit(0)

    if args.issue is None:
        print('''<issue> isn't specified''')
        print('usage: ' + use_as_os_command.__doc__)
        sys.exit(2)

    if args.status is None:
        print('''<status> isn't specified''')
        print('usage: ' + use_as_os_command.__doc__)
        sys.exit(2)

    status_id = get_status_identifier_by_name(args.status)
    if status_id is None:
        sys.exit(1)

    if update_status_issue(args.issue, status_id, args.notes) != 200:
        print('''Status has not been updated''')
        sys.exit(1)


if __name__ == '__main__':
    redmine_host_project = 'http://redmine.tomsksoft/tomsksoft'
    redmine_access_key = os.environ["REDMINE_API_ACCESS_KEY"]
    use_as_os_command()
