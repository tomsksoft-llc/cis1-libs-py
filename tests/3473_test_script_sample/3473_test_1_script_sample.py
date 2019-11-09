import sys
sys.path.append('../')
import lib_test_runner


if __name__ == '__main__':
    res = 0
    if lib_test_runner.run(['../../cis1-libs/script_sample.py', '-v'], "must be OK") != 0:
        res = 2
    if lib_test_runner.run(['../../cis1-libs/script_sample.py', '-e'], "must be ERROR") == 0:
        res = 2
    if lib_test_runner.run(['../../cis1-libs/script_sample.py', '-h'], "must be OK") != 0:
        res = 2
    if lib_test_runner.run(['../../cis1-libs/script_sample.py', 'foo', 'bar'], "must be ERROR") == 0:
        res = 2

    if res == 0:
        lib_test_runner.ok()
    else:
        lib_test_runner.fail()
