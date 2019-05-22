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

def check_code(code):
    if code == 1:
        print('Program have exceptions')
        raise SystemExit(1)

if '__main__':
    url = 'https://deskroll.com/'

    print('Checking depth error...')
    depth_res, depth_code = check(url, 0, 'False')
    check_code(depth_code)
    print('Depth check result:\n', depth_res)

    print('Checking external error...')
    external_res, external_code = check(url, 1, 'Folse')
    check_code(external_code)
    print('External check result:\n', external_res)
    print('Checking parameters error...')
    parameters_res, parameters_code = check('', '', '')
    check_code(parameters_code)
    print('Parameters check result:\n', parameters_res)
    print('Checking --help usage:')
    help_res, help_code = check('--help', '', '')
    check_code(help_code)
    print('Help checking  result:\n', help_res)




    correct = True
    if (('list index out of range' in parameters_res) or ('invalid literal for int()' in parameters_res)) and ('usage' in parameters_res):
        print('Parameters check successful')
    else:
        correct = False
        print('Parameters check is not correct')
    if (('depth must be > 0' in depth_res) or ('invalid literal for int()' in depth_res)) and ('usage' in depth_res):
        print('Depth check successful')
    else:
        correct = False
        print('Depth check is not correct')
    if ('External must be True or False' in external_res) and ('usage' in external_res):
        print('External check successful')
    else:
        correct = False
        print('External check is not correct')
    if 'usage' in help_res:
        print('Help check successful')
    else:
        correct = False
        print('Help check is not correct')

    if correct:
        raise SystemExit(0)
    else:
        raise SystemExit(1)

