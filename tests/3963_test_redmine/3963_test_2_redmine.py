import sys
import lib_test_runner
import redmine

if __name__ == '__main__':
    _res = 0
    if redmine.get_status_identifier_by_name('blaaaa') == 0:
        _res = 2
    if redmine.update_status_issue('invalid_issue', -1, '') == 0:
        _res = 2
    if redmine.update_status_issue('invalid_issue', 1, '') == 0:
        _res = 2
    if redmine.update_status_issue('invalid_issue', 1, 'note test') == 0:
        _res = 2

    if _res == 0:
        lib_test_runner.test_ok()
    else:
        lib_test_runner.test_fail()
