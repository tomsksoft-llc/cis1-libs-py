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
# FILE: git_scm.py
# Authors: Maxim Felchuck, Ilya Bezkhodarnov
#
##############################################################################
'''It is a script for downloading git repositories and checkout to specified
branch or commit. By default checkout to master.

'''

import sys
import subprocess
import os
import argparse


def download_repository(repository_url, repository_dir, ref):
    '''Download git repository and checkout to specified ref

    Args:
        repository_url: Long string repository url
        repository_dir: short string folder name
        ref_name: branch name or commit hash (by default = master)

    Returns:
        0: on success
       -1: if fail
    '''
    res = subprocess.run(['git', 'clone', repository_url,
                          repository_dir], check=True).returncode
    if res != 0:
        return -1
    os.chdir(repository_dir)

    res = subprocess.run(['git', 'checkout', ref], check=True).returncode
    if res != 0:
        return -1

    return 0


def use_as_os_command():
    ''' git_scm.py <repo> <dir> [ref]

    repo - URI to git repository
    dir - directory where repo will be downloaded
    ref - branch name or commit hash, if not specified "master" will be used

    Return value:
        0 - on success
        non zero - if any error
    '''
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-h', '--help', action='store_true')
    parser.add_argument("repo", nargs="?")
    parser.add_argument("dir", nargs="?")
    parser.add_argument("ref", nargs='?', default='master')
    parser.usage = use_as_os_command.__doc__

    args = parser.parse_args()

    if args.help:
        print('usage: ' + use_as_os_command.__doc__)
        sys.exit(0)

    if args.repo is None:
        print('''<repo> isn't specified''')
        print('usage: ' + use_as_os_command.__doc__)
        sys.exit(2)

    if args.dir is None:
        print('''<dir> isn't specified''')
        print('usage: ' + use_as_os_command.__doc__)
        sys.exit(2)
    if os.path.exists(args.dir):
        print('''path "{0}" already exists'''.format(args.dir))
        print('usage: ' + use_as_os_command.__doc__)
        sys.exit(2)

    res = download_repository(args.repo, args.dir, args.ref)
    return res


if __name__ == '__main__':
    use_as_os_command()
