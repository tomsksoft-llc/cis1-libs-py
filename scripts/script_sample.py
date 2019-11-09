##############################################################################
#
# Copyright (c) 2109 TomskSoft LLC
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
# Author: Ilya Bezkhodarnov
#
##############################################################################
'''It is a sample of a script that meets all requiremens for CI Python Libs.

See devguide.md in the dir 'docs' of the library repository for all
requirements and other details.

'''

import sys
import argparse
import ci_py_lib_version

def script_sample(option=""):
    '''Usage as python module

    Depending on option value do:
        '-v': print module version number, return 0
        '-e': print 'ERROR', return 1
        '-h': print help message, return 0
        in any other case: print help message, return 2

    Args:
        option:  may be '-v', '-e', '-h'

    Returns:
        0: if option in '-v', '-h'
        1: if option is '-e'
        2: if option is any other
    '''
    if option == '-h':
        print(script_sample.__doc__)
        return 0
    if option == '-v':
        print(ci_py_lib_version.CI_PY_LIB_VERSION)
        return 0
    if option == '-e':
        print('ERROR')
        return 1
    print(script_sample.__doc__)
    return 2

def use_as_os_command():
    ''' script_sample.py [COMMAND]

    COMMAND
        -v, --version
            print version of the script and exit with code 0
        -e, --error
            print 'ERROR' and exit with code 1
        -h, --help
            print help message and exit with 0

    DEFAULT
        print help message and exit with 2
    '''
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-v', '--version', action='store_true')
    parser.add_argument('-e', '--error', action='store_true')
    parser.add_argument('-h', '--help', action='store_true')
    parser.usage = use_as_os_command.__doc__
    option = parser.parse_args()

    if option.help:
        print('usage: '+use_as_os_command.__doc__)
        sys.exit(0)
    if option.version == option.error:
        print('usage: '+use_as_os_command.__doc__)
        sys.exit(2)
    if option.version:
        arg = '-v'
    else:
        arg = '-e'

    res = script_sample(arg)
    sys.exit(res)

if __name__ == '__main__':
    use_as_os_command()
