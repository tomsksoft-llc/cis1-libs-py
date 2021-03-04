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


def showing_an_issue(issue, status=None, tracker=None):
    """Verify an issue used by redmine the project.

issue string: The issue is bound in redmine.
status string: The issue status.
tracker string: The issue tracker.

Return value:
    If a issue is exist, and the status and/or of tracker  matched, returned true.
    If a issue is exist, but the status of tracker does not match, returned false.
    If such a issue is not found, or not possible to process the request, returned None.
    """
    req = Request('%s/issues/%s.json' % (_service_host_project(), issue))
    req.add_header('X-Redmine-API-Key', _service_access_key())
    try:
        content = urlopen(req).read()
    except URLError as err:
        print('We failed to reach a server.')
        print('Reason: ', err.reason)
        return None

    data = json.loads(content.decode('utf-8'))
    if status is not None and data['issue']['status']['name'] != status:
        print("The issue status '%s' does not exist." % status)
        return False

    if tracker is not None and data['issue']['tracker']['name'] != tracker:
        print("The tracker status '%s' does not exist." % tracker)
        return False

    return True


def get_status_identifier_by_name(status_name):
    """Returns the status ID for the specified name used by redmine the project.

    status_name string: A string for the status name.

    Return value:
        If such a status is not found, or not possible to process the request, returned None.
    """
    req = Request('%s/issue_statuses.json' % _service_host_project())
    req.add_header('X-Redmine-API-Key', _service_access_key())
    try:
        content = urlopen(req).read()
    except URLError as err:
        print('We failed to reach a server.')
        print('Reason: ', err.reason)
        return None
    else:
        data = json.loads(content.decode('utf-8'))
    try:
        return list(filter(
            lambda x: x['name'].upper() == status_name.upper(), data['issue_statuses']))[0]['id']
    except IndexError:
        print("The issue status '%s' does not exist." % status_name)


def update_status_issue(issue, status_id, notes):
    """Request to change the status of a problem in a redmine project.

    'issue': A hash of the issue is bound to a redmine project.
    'status_id': Id status used by redmine the project.
    'notes': Comments about the update.

    Return value:
       0 - on success
       non zero - HTTP protocol errors are valid responses.
    """
    values = '''{ "issue": { "status_id": "%s", "notes": "%s" } }''' % (status_id, notes)
    req = Request(
        '%s/issues/%s.json' % (_service_host_project(), issue), data=values.encode(), method='PUT')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Redmine-API-Key', _service_access_key())
    try:
        with urlopen(req) as context:
            pass
        return 0 if context.code == 200 else context.code
    except HTTPError as err:
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', err.code)
    except URLError as err:
        print('We failed to reach a server.')
        print('Reason: ', err.reason)


def _service_host_project():
    # Returns the host project passed through the system variable,
    # if it is absent, returns the default value.
    if 'REDMINE_HOST_PROJECT' in os.environ:
        return os.environ["REDMINE_HOST_PROJECT"]
    return "https://"


def _service_access_key():
    # Returns the access key passed through the system variable,
    # if it is absent, returns the empty value.
    if 'REDMINE_API_ACCESS_KEY' in os.environ:
        return os.environ["REDMINE_API_ACCESS_KEY"]
    return ""


def use_as_os_command():
    """redmine.py <issue> <status> [notes]
set status in issue and comments

    issue - A hash of the issue is bound to a project.
    status - Set status workflow, of the exist in redmine project
    notes - Comments about the update


redmine.py <issue> [-s | --status <status>] [-t | --tracker <tracker>]
verify exist of the issue, its status and tracker

    issue - A hash of the issue is bound to a project.
    status - verify issue status.
    tracker - verify issue tracker.

Return value:
    0 - on success
    non zero - if any error
    """
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-h', '--help', action='store_true')
    parser.add_argument("issue", nargs="?")
    parser.add_argument("set_status", nargs="?")
    parser.add_argument("notes", nargs='?', default='')
    parser.add_argument('-t', '--tracker', nargs="?")
    parser.add_argument('-s', '--status', nargs="?")
    parser.usage = use_as_os_command.__doc__

    args = parser.parse_args()

    if args.help:
        print('usage: ' + use_as_os_command.__doc__)
        sys.exit(0)

    if args.issue is None:
        print('''<issue> isn't specified''')
        print('usage: ' + use_as_os_command.__doc__)
        sys.exit(2)

    if args.set_status is None:
        if showing_an_issue(args.issue, args.status, args.tracker):
            print('''This issue #%s exists''' % args.issue)
            sys.exit(0)

        sys.exit(1)

    status_id = get_status_identifier_by_name(args.set_status)

    if status_id is None:
        sys.exit(1)

    if update_status_issue(args.issue, status_id, args.notes) != 0:
        print('''Status has not been updated''')
        sys.exit(1)


if __name__ == '__main__':
    use_as_os_command()
