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
import the script to test script and use its function ro start utility as
os command and when exit from test script to indicate error or success
'''
from typing import List
import subprocess
import sys

import lib_config


_OK = 'OK'
_ERR = 'FAIL'


def run(args: List[str], msg: str = None):
    '''Use the function for test utility via os command

    Args:
     args - command line argiments started from testing script name
     msg - message for showing in test report

    Returns:
     Exit code from utility

    '''
    args = [lib_config.PYTHON3] + args
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    code = proc.returncode
    proc.terminate()
    args_str = ' '.join(args)
    if code:
        print(f"{_ERR:.<10}{msg:.^30}{args_str:.>30}")
        print(stdout.decode('utf-8'))
        print(stderr.decode('utf-8'))
    else:
        print(f"{_OK:.<10}{msg:.^30}{args_str:.>30}")
    return code


def test_ok():
    '''Use the function when exit from test script to indicate success
    '''
    sys.exit(0)


def test_fail():
    '''Use the function when exit from test script to indicate test fail
    '''
    sys.exit(1)
