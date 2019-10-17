import subprocess
import os
import sys


# Run program and return code
def check(rep, mod_h, commit_id, mod_b, ref, dir):
    process = subprocess.Popen(
        'python ../git_scm.py {0} {1} {2} {3} {4} {5}'.format(rep, mod_h, commit_id, mod_b, ref, dir),
        stdout=subprocess.PIPE,
        shell=True)
    output = process.communicate()
    res = output[0].decode('utf8')
    code = process.poll()
    return res, code


# If program code = 1 return 1
def check_code(code):
    if code != 0:
        print('link_check.py has an error')
        raise sys.exit(1)


if '__main__':
    rep = 'git@github.com:tomsksoft-llc/cis1-libs-py.git'
    dir = 'Test_repo'
    commit_id = '82dc11400005583e5a6a860e7f5829245ca92b51'
    ref = '3441_link_check'

    # If after all parameters no dir name should be display an error
    print('Dir usage check...')
    dir_res, dir_code = check(rep, '-h', commit_id, '', '', '')
    print('Dir usage check result:\n', dir_res)
    check_code(dir_code)
    # If after the -h parameter no commit hash, then should display an error
    print('mod_h usage check...')
    mod_h_res, mod_h_code = check(rep, '-h', '', '', '', dir)
    print('mod_h usage check result:\n', mod_h_res)
    check_code(mod_h_code)
    # If after the -b parameter no branch name, then should display an error
    print('mod_b usage check...')
    mod_b_res, mod_b_code = check(rep, '', '', '-b', '', dir)
    print('mod_b usage check result:\n', mod_b_res)
    check_code(mod_b_code)
    # If are not enough parameters, then should display an error
    print('Parameters usage check...')
    parameters_res, parameters_code = check('', '', '', '', '', '')
    check_code(parameters_code)
    print('Parameters usage check result:\n', parameters_res)
    # --help usage check and check his return code
    print('Checking --help usage:')
    help_res, help_code = check('--help', '', '', '', '', '')
    check_code(help_code)
    print('--help usage check result:\n', help_res)

    # Return codes should include usage and error pointers depending on the type of verification
    correct = True
    if ("usage" in dir_res) and (("fatal:the last argument should be <dir>" in dir_res)
                                 or ("After argument '-h' must be 'commit_id'" in dir_res)
                                 or ("After argument '-b' must be 'ref'" in dir_res)):
        print("Dir usage check successful")
    else:
        correct = False
        print('Dir check is not correct')
    if ("usage" in mod_h_res) and ("After argument '-h' must be 'commit_id'" in mod_h_res):
        print("mod_h usage check successful")
    else:
        correct = False
        print('mod_h check is not correct')
    if ("usage" in mod_b_res) and ("After argument '-b' must be 'ref'" in mod_b_res):
        print("mod_b usage check successful")
    else:
        correct = False
        print('mod_b check is not correct')
    if ('usage' in parameters_res) and ('list index out of range' in parameters_res):
        print('Parameters check successful')
    else:
        correct = False
        print('Parameters check is not correct')
    if 'usage' in help_res:
        print('Help check successful')
    else:
        correct = False
        print('Help check is not correct')
    # If at least one return code is not correct return 1
    if correct:
        raise sys.exit(0)
    else:
        raise sys.exit(1)
