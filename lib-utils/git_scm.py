import sys
import subprocess
import os
import re


def download_repository(branch, commit_id, repository_url, repository_dir):
    """Download git repository
    By given repository branch, commit hash, repository dir
    :param branch: short string branch name. May be specified, or may be False.
    :param commit_id: shot or long string commit hash. May be specified, or may be False.
    :param repository_url: Long string repository url.
    :param repository_dir: Short string repository folder name.
    :return: Nothing.
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


def main(args):
    try:
        if (args[1] == '--help') or (args[1] == '-h'):
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
        repository_dir = args[-1:][0]
        repository_url = args[1]
        args_sum = len(args)
        hash_pattern = '[0-9a-f]{5,40}'

        if args_sum == 5:
            branch = args[2]
            commit_id = args[3]
        elif args_sum == 4:
            if re.match(hash_pattern, args[2]) is not None:
                commit_id = args[2]
            else:
                branch = sys.argv[2]
        elif (args_sum < 3) or (args_sum > 5):
            usage()
            raise Exception('Attribute error')

        if not os.path.isdir(repository_dir):
            download_repository(branch, commit_id, repository_url, repository_dir)
        else:
            raise Exception('fatal: path "{0}" already exists.'.format(repository_dir))

    except Exception as err:
        print(err)
        sys.exit(2)


if __name__ == '__main__':
    main(sys.argv)
