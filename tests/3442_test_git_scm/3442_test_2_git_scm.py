import subprocess
import os
import sys

sys.path.append('../')
import lib_test_runner


# Run program and return code

def create_test_repo():
    subprocess.run(['git', 'init', 'TestRepo'], check=False)
    os.chdir('TestRepo')
    subprocess.run(['git', 'checkout', '-b', 'TestBranch'], check=False)
    with open('readme.txt', 'w'):
        pass
    subprocess.run(['git', 'add', 'readme.txt'], check=False)
    subprocess.run(['git', 'commit', '-m', 'TestCommit'], check=False)
    process = subprocess.Popen(['git', 'rev-parse', '--verify', 'HEAD'],
                               stdout=subprocess.PIPE, shell=False)
    output = process.communicate()
    commit_id = output[0].decode('utf8')
    commit_id = commit_id[:-2]
    os.chdir('..')
    return commit_id


def main():
    commit_id = create_test_repo()
    res = lib_test_runner.run(['../../lib-utils/git_scm.py',
                               'TestRepo', 'TestBranch',
                               commit_id, 'TestDir'], "Work check")
    if res:
        lib_test_runner.test_fail()
    else:
        lib_test_runner.test_ok()


if __name__ == "__main__":
    main()
