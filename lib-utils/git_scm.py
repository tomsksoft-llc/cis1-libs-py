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
# Authors: Maxim Felchuck
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

    null = open(os.devnull, 'w')
    try:
        subprocess.run(['git', 'clone', repository_url,
                        repository_dir], check=False)
        os.chdir(repository_dir)
        subprocess.run(['git', 'checkout', ref], check=False)

        subprocess.run(['git', 'reset', '--hard'],
                       stdout=null, check=False)

        subprocess.run(['git', 'clean', '-fdx'],
                       stdout=null, check=False)

        subprocess.run(['git', 'fetch', '--tags', '--progress',
                        repository_url, '+refs/heads/*:refs/remotes/origin/*'],
                       stdout=null, check=False)

        subprocess.run(['git', 'config', 'core.sparsecheckout'],
                       stdout=null, check=False)

        subprocess.run(['git', 'checkout', '-f', ref],
                       stdout=null, check=False)
    except:
        print('usage: ' + use_as_os_command.__doc__)
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
    parser = argparse.ArgumentParser(add_help=True, usage='usage:  git_scm.py <repo> <dir> [ref]')
    parser.add_argument("repo", help='- URI to git repository')
    parser.add_argument("dir", help='- directory where repo will be downloaded')
    parser.add_argument("ref", nargs='?', default='master',
                        help='- branch name or commit hash, if not specified "master" will be used')
    args = parser.parse_args()
    if os.path.exists(args.dir):
        print('usage: ' + use_as_os_command.__doc__)
        print('fatal:  path "{0}" already exists.'.format(args.dir))
        sys.exit(2)
    res = download_repository(args.repo, args.dir, args.ref)
    sys.exit(res)


if __name__ == '__main__':
    use_as_os_command()
