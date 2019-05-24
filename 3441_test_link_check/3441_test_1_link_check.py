import subprocess
import os
import sys
from builtins import SystemExit

# Run program and return code
def check(url, depth, external):
    process = subprocess.Popen('python ../link_check.py {0} {1} {2}'.format(url,depth,external), stdout=subprocess.PIPE, shell=True)
    output = process.communicate()
    res = output[0].decode('utf8')
    code = process.poll()
    return res, code
# If program code = 1 return 1
def check_code(code):
    if code == 1:
        print('link_check.py has an error')
        raise SystemExit(1)

if '__main__':
    url = 'https://deskroll.com/'
# Depth usage check and check his return code
    print('Depth usage check...')
    depth_res, depth_code = check(url, 0, 'False')
    check_code(depth_code)
    print('Depth usage result:\n', depth_res)

# External usage check and check his return code
    print('External usage check...')
    external_res, external_code = check(url, 1, 'Folse')
    check_code(external_code)
    print('External usage result:\n', external_res)

# Parameters usage check and check his return code
    print('Parameters usage check...')
    parameters_res, parameters_code = check('', '', '')
    check_code(parameters_code)
    print('Parameters usage check result:\n', parameters_res)

# --help usage check and check his return code
    print('Checking --help usage:')
    help_res, help_code = check('--help', '', '')
    check_code(help_code)
    print('--help usage check result:\n', help_res)

# Return codes should include usage and error pointers depending on the type of verification
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

# If at least one return code is not correct return 1
    if correct:
        raise SystemExit(0)
    else:
        raise SystemExit(1)

