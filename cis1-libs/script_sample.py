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
'''It is a sample of a script that meets all requiremens for CIS Python Libs.

See devguide.md in the dir 'docs' of the library repository for all
requirements and other details.

SCRIPT USAGE
	script_sample.py <-v|--version|-e|--error|-h|--help>

	-v, --version
		print version of the script and exit with code 0

	-e, --error
		print "ERROR" and exit with code 1

	-h, --help
		print usage and exit with 0

	by default
		print usage and exit with 2

PYTHON USAGE
	script_sample(option)

	where option may be:
		'-v':	print version of the module and return 0

		'-e':	print ERROR and return 1

		'-h':	print usage and return 0

		in any other case:
			print usage and return 2

'''

import sys
import argparse

_VERSION = "1.0.0"

def script_sample(option=""):
    '''Sample main script function

    Do somthing depend on option value. See "PYTHON USAGE" section for details.

    Args:
        option: String, empty by default. Possible values: "-v", "-e", "-h",
            "--help".

    Returns:
        0: if option in '-v', '-h';
        1: if option is '-e';
        2: if option is any other.
        See "PYTHON USAGE" section for details.

    '''
    if option == '-v':
        print(_VERSION)
        return 0
    if option == '-e':
        print('ERROR')
        return 1
    _print_usage()
    return 2

def _print_usage():
    print(__doc__)

def _main():
    '''Command line interface to script function

    1) Parse command line.
    2) Check its sinopsys.
    3) Convert command line arguments to properly values for call script
       function.
    4) Call to script function, check result and define is it SUCCESS or FAIL.
    5) Exit with code depeds on script function call result.

    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', action='store_true')
    parser.add_argument('-e', '--error', action='store_true')
    parser.usage = __doc__
    try:
        option = parser.parse_args()
    except Exception as err:
        _print_usage()
        print(err)
        sys.exit(2)

    if option.version == option.error:
        _print_usage()
        sys.exit(2)
    elif option.version:
        arg = '-v'
    else:
        arg = '-e'

    try:
        res = script_sample(arg)
    except Exception as err:
        res = 3
        print(err)

    sys.exit(res)

if __name__ == '__main__':
    _main()
