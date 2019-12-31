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
# FILE: gitlab.py
# Authors: Dmitriy Tsvedel
#
##############################################################################
'''This is a script for creating request merge a branch in Gitlab.
You can also assign a responsible user (Optional).

'''

import os
import sys
import json
import argparse
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


def merge_request(source_branch, target_branch, assignee):
    """merge_request <source_branch> <target_branch> [assignee]
     Creates a new merge request.

    'source_branch': The source branch.
    'target_branch': The target branch.
    'assignee': Assignee user ID (no required).

    Return value:
       0 - on success
       non zero - HTTP protocol errors are valid responses.
    """
    values = json.dumps(dict(
        id=_service_host_project(),
        source_branch=source_branch,
        target_branch=target_branch,
        title="Merge %s to %s" % (source_branch, target_branch),
        assignee_id=assignee,
        remove_source_branch=True
    ))
    req = Request('%s/merge_requests' % _service_host_project(), data=values.encode())
    req.add_header('Content-Type', 'application/json')
    req.add_header('PRIVATE-TOKEN', _service_access_key())
    try:
        with urlopen(req) as context:
            pass
        return 0 if context.code == 201 else context.code
    except HTTPError as err:
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', err.code)
    except URLError as err:
        print('We failed to reach a server.')
        print('Reason: ', err.reason)


def _service_host_project():
    # Returns the host project passed through the system variable,
    # if it is absent, returns the default value.
    if 'GITLAB_HOST_PROJECT' in os.environ:
        return os.environ["GITLAB_HOST_PROJECT"]
    return "http://"


def _service_access_key():
    # Returns the access key passed through the system variable,
    # if it is absent, returns the empty value.
    if 'GITLAB_API_ACCESS_KEY' in os.environ:
        return os.environ["GITLAB_API_ACCESS_KEY"]
    return ""


def use_as_os_command():
    """gitlab.py merge_request <source_branch> <target_branch> [assignee]

    issue - A hash of the issue is bound to a project.
    status - Status workflow. Issues reports should show only statuses used by the project
    notes - Comments about the update

    Return value:
       0 - on success
       non zero - if any error
    """
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-h', '--help', action='help')
    parser.add_argument('--merge_request', nargs='*')
    parser.usage = use_as_os_command.__doc__

    args = parser.parse_args()

    # globals()[sys.argv[1]]()

    if args.merge_request is not None:
        params = dict(enumerate(args.merge_request))

        if params.get(0) is None:
            print('''<source_branch> isn't specified''')
            print('usage: ' + use_as_os_command.__doc__)
            sys.exit(2)

        if params.get(1) is None:
            print('''<target_branch> isn't specified''')
            print('usage: ' + use_as_os_command.__doc__)
            sys.exit(2)

        if merge_request(params.get(0), params.get(1), params.get(3, "")) != 0:
            print('''Merge request not created.''')
            sys.exit(1)


if __name__ == '__main__':
    use_as_os_command()
