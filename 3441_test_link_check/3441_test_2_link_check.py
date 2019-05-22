import subprocess
import os
import sys
from builtins import SystemExit


def check(url, depth, external):
    os.chdir('..')
    process = subprocess.Popen('.\link_check.py {0} {1} {2}'.format(url,depth,external), stdout=subprocess.PIPE, shell=True)
    output = process.communicate()
    res = output[0].decode('utf8')
    code = process.poll()
    os.chdir('3441_test_link_check')
    return res, code

if '__main__':
    url = 'https://deskroll.com/'
    depth = 2
    external = 'False'
    res, code = check(url,depth,external)
    print(res)
    if code == 1:
        print('Program have exceptions')
        raise SystemExit(1)
    else:
        print('Program worked correctly')
        raise SystemExit(0)