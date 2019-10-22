import sys
sys.path.append('../')
import lib_test_runner

# Run program and return code
def run_program(depth, external):
    url = 'https://deskroll.com/'
    res = lib_test_runner.run(['../link_check.py', url, depth, external], "Message for report")
    return res

if '__main__':
    status = True
    # Depth usage check
    res = run_program('0', 'False')
    if res == 2:
        print('Depth usage check successful')
    else:
        print('Depth usage check incorrect')
        status = False
    # External usage check
    res = run_program('1', 'Folse')
    if res == 2:
        print('External usage check successful')
    else:
        print('External usage check incorrect')
        status = False
    # Parameters usage check
    res = run_program('', '')
    if res == 2:
        print('Parameters usage check successful')
    else:
        print('Parameters usage check incorrect')
        status = False
    # Final check
    if status:
        print('All checks successful')
        lib_test_runner.ok()
    else:
        print('Check have error')
        lib_test_runner.fail()

