import subprocess
import os
import sys
# Run program and return code
def check(rep, mod_h, commit_id, mod_b, ref, dir):   
    process = subprocess.Popen('python ../git_scm.py {0} {1} {2} {3} {4} {5}'.format(rep, mod_h, commit_id, mod_b, ref, dir),
                               stdout=subprocess.PIPE,
                               shell=True)
    output = process.communicate()
    res = output[0].decode('utf8')
    code = process.poll()
    return res, code
# If program code = 1 return 1
def check_code(code):
    if code == 1:
        print('link_check.py has an error')
        raise sys.exit(1)
if '__main__':
    rep = 'git@github.com:tomsksoft-llc/cis1-libs-py.git'
    dir = 'Test_repo'
    commit_id = '82dc11400005583e5a6a860e7f5829245ca92b51'
    ref = '3441_link_check'
    res, code = check(rep, '-h', commit_id, '-b', ref, dir)
# If program return code = 0 program works correctly
    if code == 1:
        print('Program have exceptions')
        raise sys.exit(1)
    else:
        print('Program worked correctly')
        raise sys.exit(0)
