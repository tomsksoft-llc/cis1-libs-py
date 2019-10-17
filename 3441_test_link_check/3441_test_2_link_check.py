import subprocess
import os
import sys


# Run program and return code
def check(url, depth, external):
    process = subprocess.Popen('python ../link_check.py {0} {1} {2}'.format(url, depth, external),
                               stdout=subprocess.PIPE, shell=True)
    output = process.communicate()
    res = output[0].decode('utf8')
    code = process.poll()
    return res, code


if '__main__':
    url = 'https://deskroll.com/'
    depth = 2
    external = 'False'
    res, code = check(url, depth, external)
    print(res)
    # If program return code = 0 program works correctly
    if code != 0:
        print('Program have exceptions')
        raise sys.exit(1)
    else:
        print('Program worked correctly')
        raise sys.exit(0)
