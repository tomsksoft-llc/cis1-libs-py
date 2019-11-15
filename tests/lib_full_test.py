##############################################################################
#
# Copyright (c) 2019 TomskSoft LLC
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# FILE: tests\lib_full_test.py
# Author: Egor Gribkov
#
##############################################################################
'''
Use the script lib_full_test.py from command line to start all tests
Exit code: 0 if all tests passed, !0 otherwise

'''
import sys
import subprocess
import pathlib
import re
import os

import lib_config

_OK = 'OK'
_ERR = 'FAIL'


def _get_platform():
    platforms = {
        'linux1' : 'Linux',
        'linux2' : 'Linux',
        'darwin' : 'OS X',
        'win32' : 'Windows'
    }
    if sys.platform not in platforms:
        return sys.platform
    return platforms[sys.platform]


def _run_test(cur_dir, test_file):
    proc = subprocess.Popen([lib_config.PYTHON3, test_file.name], cwd=cur_dir, \
			    stdout=subprocess.PIPE, \
                            stderr=subprocess.PIPE, env=os.environ)
    stdout, stderr = proc.communicate()
    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')
    status = proc.poll()
    if  status == 0:
        print(f"{_OK:.<10}{test_file.name:.>30}")
    else:
        print(f"{_ERR:.<10}{test_file.name:.>30}")
        print("---------------------------------------------------------------")
        print(stdout)
        print(stderr)
        print("---------------------------------------------------------------")
        print()
    proc.terminate()
    return status


def _run_all_tests():
    if _get_platform() == 'Windows':
        os.environ['PYTHONPATH'] = '..;../../lib-utils'
    else:
        os.environ['PYTHONPATH'] = '..:../../lib-utils'

    print("\nCI Python scripts lib self testing started:\n")
    f_test = open("test_lib_full_test.py")
    if _run_test(".", f_test) != 0:
        print("FATAL...........test_runner self check failed.\nExecution aborted\n\n")
        sys.exit(3)
    print("\nTests runner self test passed, starting lib scripts tests:\n")

    status = 0
    for test_dir in pathlib.Path('./').iterdir():
        if not test_dir.is_dir():
            continue
        mask = re.match(r"\d+_test_(?P<test_name>[\w_]+)", test_dir.name)
        if mask is None:
            continue
        for test_file in test_dir.iterdir():
            if not test_file.is_file():
                continue
            if not test_file.name[-3:] == '.py':
                continue
            if test_file.name == '__init__.py':
                continue
            if _run_test(test_dir, test_file) != 0:
                status = 2
    if status == 0:
        print("\nAll tests passed successfully")
    else:
        print('''\nThere are error(s) in the some test(s). See log for details.\n
                  Library testing FAILED\n\n''')
    sys.exit(status)


if __name__ == '__main__':
    _run_all_tests()
