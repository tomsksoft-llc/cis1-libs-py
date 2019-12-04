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
# Author: Felchuck Maxim
#
##############################################################################
'''It is a  script for downloading git repositories.

Downloading to the specified repository url and/or commit hash and/or the repository branch
by default get (pull and checkout) HEAD of the master branch from repo

'''

import sys
import subprocess
import os
import re
import argparse


def download_repository(branch, commit_id, repository_url, repository_dir):
    """Download git repository

    Args:
        branch: short string branch name. May be specified, or may be False.
        commit_id: shot or long string commit hash. May be specified, or may be False.
        repository_url: Long string repository url.
        repository_dir: Short string repository folder name.

    """
    null = open(os.devnull, 'w')
    if branch:
        subprocess.run(['git', 'clone', repository_url,
                        '-b', branch, repository_dir], check=False)
    else:
        subprocess.run(['git', 'clone', repository_url,
                        repository_dir], check=False)

    os.chdir(repository_dir)
    subprocess.run('git rev-parse --is-inside-work-tree',
                   stdout=null, check=False)

    if not commit_id:
        process = subprocess.Popen(['git', 'rev-parse', '--verify', 'HEAD'],
                                   stdout=subprocess.PIPE, shell=False)
        output = process.communicate()
        main_commit_id = output[0].decode('utf8')
        main_commit_id = main_commit_id[:-2]
    else:
        main_commit_id = commit_id

    subprocess.run(['git', 'reset', '--hard'],
                   stdout=null, check=False)
    subprocess.run(['git', 'clean', '-fdx'],
                   stdout=null, check=False)
    subprocess.run(['git', 'fetch', '--tags', '--progress',
                    repository_url, '+refs/heads/*:refs/remotes/origin/*'],
                   stdout=null, check=False)
    subprocess.run(['git', 'rev-parse', main_commit_id],
                   stdout=null, check=False)
    subprocess.run(['git', 'config', 'core.sparsecheckout'],
                   stdout=null, check=False)
    subprocess.run(['git', 'checkout', '-f', main_commit_id],
                   stdout=null, check=False)


def use_as_os_command():
    ''' git_scm <repo> [args] <dir>

by default get (pull and checkout) HEAD of the master branch from repo
args:
    branch - get head of the specified branch
    commit_hash - get the specified revision

Return value:

0 - if success
non zero - if any error
    '''
    hash_pattern = '[0-9a-f]{5,40}'
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("repo")
    parser.add_argument("args", nargs=argparse.REMAINDER)
    parser.add_argument("dir")
    parser.usage = use_as_os_command.__doc__
    args = parser.parse_args()
    commit_id, branch = False, False
    
    if len(args.args) == 2:
        branch = args.args[0]
        commit_id = args.args[1]
    elif len(args.args) == 1:
        if re.match(hash_pattern, args.args[0]) is not None:
            commit_id = args.args[0]
        else:
            branch = args.args[0]
    elif len(args.args) > 2:
        print('usage: ' + use_as_os_command.__doc__)
        print('git_scm.py: arguments error')
        sys.exit(2)

    download_repository(branch, commit_id, args.repo, args.dir)


if __name__ == '__main__':
    use_as_os_command()
