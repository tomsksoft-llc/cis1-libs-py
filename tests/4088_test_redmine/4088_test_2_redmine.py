import sys
import lib_test_runner
import redmine

if __name__ == '__main__':
    _res = 0
    if redmine.showing_an_issue('invalid_issue') == 0:
        _res = 2
    if redmine.showing_an_issue('invalid_issue', '') == 0:
        _res = 2
    if redmine.showing_an_issue('invalid_issue', '', '') == 0:
        _res = 2

    if _res == 0:
        lib_test_runner.test_ok()
    else:
        lib_test_runner.test_fail()
