import subprocess
import os
import sys

sys.path.append('../')
import lib_test_runner


# Run program and return code

def main():

    _res = 0
    if lib_test_runner.run(['../../lib-utils/git_scm.py',
                            'https://github.com/tomsksoft-llc/ci-py-lib.git', 'TestDir'], "Work check") != 0:
        _res = 2

    if _res == 0:
        lib_test_runner.test_ok()
    else:
        lib_test_runner.test_fail()


if __name__ == "__main__":
    main()
