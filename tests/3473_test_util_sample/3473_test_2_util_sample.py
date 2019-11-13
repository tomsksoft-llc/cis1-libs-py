import sys
import lib_test_runner
import util_sample

if __name__ == '__main__':
    _res = 0
    if util_sample.util_sample('-v') != 0:
        _res = 2
    if util_sample.util_sample('-e') == 0:
        _res = 2
    if util_sample.util_sample('-h') != 0:
        _res = 2
    if util_sample.util_sample('foo bar') == 0:
        res = 2

    if _res == 0:
        lib_test_runner.ok()
    else:
        lib_test_runner.fail()
