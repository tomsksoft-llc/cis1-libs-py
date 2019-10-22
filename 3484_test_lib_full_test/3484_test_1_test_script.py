import lib_test_runner

if __name__ == '__main__':
    print("Testing some complex thing.")
    res = lib_test_runner.run(['../test_script.py', '0'], "Some happy message")

    print("Some more testing")
    res = lib_test_runner.run(['../test_script.py', '0'], "Some happy message 2")

    print('Fail this time')
    res = lib_test_runner.run(['../test_script.py', '1'], "Sad message")

    if res:
        lib_test_runner.fail()
    else:
        lib_test_runner.ok()
