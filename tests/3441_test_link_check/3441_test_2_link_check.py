import sys
import lib_test_runner

if '__main__':
    url = 'https://deskroll.com/'
    depth = '1'
    external = 'False'
    res = lib_test_runner.run(['../../lib-utils/link_check.py', url, depth, external], "Work check")
    if res == 0:
        lib_test_runner.test_ok()
    else:
        lib_test_runner.test_fail()
