import sys
import subprocess
import os
import re


def download_repository():
    FNULL = open(os.devnull, 'w')
    if branch:
        subprocess.run(['git', 'clone', repository_url, '-b', branch, repository_dir])
    else:
        subprocess.run(['git', 'clone', repository_url, repository_dir])

    os.chdir(repository_dir)
    subprocess.run('git rev-parse --is-inside-work-tree', stdout=FNULL)

    if not commit_id:
        process = subprocess.Popen(['git', 'rev-parse', '--verify', 'HEAD'], stdout=subprocess.PIPE, shell=False)
        output = process.communicate()
        main_commit_id = output[0].decode('utf8')
        main_commit_id = main_commit_id[:-2]
    else:
        main_commit_id = commit_id

    subprocess.run(['git', 'reset', '--hard'], stdout=FNULL)
    subprocess.run(['git', 'clean', '-fdx'], stdout=FNULL)
    subprocess.run(['git', 'fetch', '--tags', '--progress', repository_url, '+refs/heads/*:refs/remotes/origin/*'], stdout=FNULL)
    subprocess.run(['git', 'rev-parse', main_commit_id], stdout=FNULL)
    subprocess.run(['git', 'config', 'core.sparsecheckout'], stdout=FNULL)
    subprocess.run(['git', 'checkout', '-f', main_commit_id], stdout=FNULL)


def usage():
    print("""
usage:

git_scm <repo> [branch]|[commit_hash] <dir>

by default get (pull and checkout) HEAD of the master branch from repo

branch - get head of the specified branch
commit_hash - get the specified revision

Return value:

0 - if success
non zero - if any error
""")


if '__main__':
    try:
        if (sys.argv[1] == '--help') or (sys.argv[1] == '-h'):
            print('''

git_scm.py - Download git repository.

Usage: git_scm <repo> [branch]|[commit_hash] <dir>

Description:
Download git repository. By commit hash or/and branch name.

''')
            sys.exit(0)
    except Exception as err:
        print(err)
        usage()
        sys.exit(2)
    try:
        commit_id, branch = False, False
        repository_dir = sys.argv[-1:][0]
        repository_url = sys.argv[1]
        hash = '[0-9a-f]{5,40}'
        if len(sys.argv) == 5:
            branch = sys.argv[2]
            commit_id = sys.argv[3]
        elif len(sys.argv) == 4:
            if re.match(hash, sys.argv[2]) is not None:
                commit_id = sys.argv[2]
            else:
                branch = sys.argv[2]
        elif (len(sys.argv) < 3) or (len(sys.argv) > 5):
            usage()
            raise Exception('Attribute error')

        if not os.path.isdir(repository_dir):
            download_repository()
        else:
            raise Exception('fatal: path "{0}" already exists.'.format(repository_dir))
        
    except Exception as err:
        print(err)
        sys.exit(2)
