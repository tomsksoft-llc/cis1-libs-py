import sys
import subprocess
import os


def download_repository():
    FNULL = open(os.devnull, 'w')
    if mod_b:
        subprocess.run(['git', 'clone', repository_url, '-b', branch, repository_dir])
    else:
        subprocess.run(['git', 'clone', repository_url, repository_dir])

    os.chdir(repository_dir)
    subprocess.run('git rev-parse --is-inside-work-tree', stdout=FNULL)

    if not mod_h:
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
    subprocess.run(['git', 'checkout', '-f', commit_id], stdout=FNULL)


def usage():
    print("""
usage:

git_scm <repo> [-b branch]|[-h commit_hash] <dir>

by default get (pull and checkout) HEAD of the master branch from repo

-b bransh - get head of the specified branch
-h commit_hash - get the specified revision

Return value:

0 - if success
non zero - if any error
""")


if '__main__':
    try:
        if (sys.argv[1] == '--help') or (sys.argv[1] == '-h'):
            print('''

git_scm.py - Dwnload git repository.

Usage: git_scm <repo> [-b branch]|[-h commit_hash] <dir>

Description:
Download git repository. By commit hash or/and branch name.

''')
            sys.exit(0)
    except Exception as err:
        print(err)
        usage()
        sys.exit(2)
    try:
        mod_h, mod_b, commit_id, branch = False, False, False, False
        repository_dir = sys.argv[-1:]
        repository_dir = repository_dir[0]

        for arg in range(len(sys.argv)):
            if sys.argv[arg] == '-h':
                try:
                    mod_h = True
                    commit_id = sys.argv[arg + 1]
                    sys.argv[arg + 1] = None
                except:
                    raise Exception("After argument '-h' must be 'commit_id'")
                if commit_id == repository_dir:
                    raise Exception("After argument '-h' must be 'commit_id'")
            if sys.argv[arg] == '-b':
                try:
                    mod_b = True
                    branch = sys.argv[arg + 1]
                    sys.argv[arg + 1] = None
                except:
                    raise Exception("After argument '-b' must be 'ref'")
                if branch == repository_dir:
                    raise Exception("After argument '-b' must be 'ref'")


        repository_url = sys.argv[1]
        args = [
            repository_url,
            mod_h,
            mod_b,
            commit_id,
            branch,
        ]
        if (repository_dir is None) or (repository_dir in args):
            raise Exception("fatal:the last argument should be <dir>")
        download_repository()
        
    except Exception as err:
        print(err)
        usage()
        sys.exit(2)
