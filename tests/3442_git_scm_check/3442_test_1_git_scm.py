import sys
import subprocess
import os
sys.path.append('../')
import lib_test_runner

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
    status = True
    commit_id = str(create_test_repo())
    # Dir usage check
    res = lib_test_runner.run(['../../cis1-libs/git_scm.py', 'TestRepo'], "Dir usage check ")
    if res != 2:
        status = False
    # No 'ref' after '-b' option
    res = lib_test_runner.run(['../../cis1-libs/git_scm.py', 'TestRepo', '-b', 'TestDir'], "Check with no 'ref' after '-b' option ")
    if res != 2:
        status = False
    # No 'commit_id' after '-h' option
    res = lib_test_runner.run(['../../cis1-libs/git_scm.py', 'TestRepo', '-h', 'TestDir'], "Check with no 'commit_id' after '-h' option ")
    if res != 2:
        status = False
    # Parameters usage check
    res = lib_test_runner.run(['../../cis1-libs/git_scm.py'], "Check without parameters ")
    if res != 2:
        status = False
    if status:
        lib_test_runner.ok()
    else:
        lib_test_runner.fail()
