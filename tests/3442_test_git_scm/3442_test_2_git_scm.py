import subprocess
import os
import sys
sys.path.append('../')
import lib_test_runner


# Run program and return code

def create_test_repo():
    subprocess.run(['git', 'init', 'TestRepo'])
    os.chdir('TestRepo')
    subprocess.run(['git', 'checkout', '-b', 'TestBranch'])
    file = open('readme.txt', 'w')
    file.close()
    subprocess.run(['git', 'add', 'readme.txt'])
    subprocess.run(['git', 'commit', '-m', 'TestCommit'])
    process = subprocess.Popen(['git', 'rev-parse', '--verify', 'HEAD'], stdout=subprocess.PIPE, shell=False)
    output = process.communicate()
    commit_id = output[0].decode('utf8')
    commit_id = commit_id[:-2]
    os.chdir('..')
    return commit_id


if '__main__':
    commit_id = create_test_repo()
    res = lib_test_runner.run(['../../lib-utils/git_scm.py', 'TestRepo', 'TestBranch', commit_id, 'TestDir'], "Work check")
    if res:
        lib_test_runner.fail()
    else:
        lib_test_runner.ok()

