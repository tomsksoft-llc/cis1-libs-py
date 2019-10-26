import lib_test_runner

if __name__ == '__main__':
    res = 0
    if lib_test_runner.run(['test_script.py', '0'], "must be OK") != 0:
        res = 2

    if lib_test_runner.run(['test_script.py', '1'], "must be FAIL") == 0:
        res = 2

    if res == 0:
        lib_test_runner.ok()
    else:
        lib_test_runner.fail()
