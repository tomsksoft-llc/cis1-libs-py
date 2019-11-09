import sys
sys.path.append('../')
import lib_test_runner
sys.path.append('../../scripts')
import script_sample

if __name__ == '__main__':
    _res = 0
    if script_sample.script_sample('-v') != 0:
        _res = 2
    if script_sample.script_sample('-e') == 0:
        _res = 2
    if script_sample.script_sample('-h') != 0:
        _res = 2
    if script_sample.script_sample('foo bar') == 0:
        res = 2

    print(_res)
    if _res == 0:
        lib_test_runner.ok()
    else:
        lib_test_runner.fail()
