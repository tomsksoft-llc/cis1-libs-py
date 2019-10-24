import sys
sys.path.append('../')
import lib_test_runner

# Run program and return code
def run_program(depth, external):
    url = 'https://deskroll.com/'
    res = lib_test_runner.run(['../link_check.py', url, depth, external], "Check usages")
    return res

if '__main__':
    status = True
    # Depth usage check
    res = run_program('0', 'False')
    if res !- 2:
        status = False
    # External usage check
    res = run_program('1', 'Folse')
    if res != 2:
        status = False
    # Parameters usage check
    res = run_program('', '')
    if res != 2:
        status = False
    # Final check
    if status:
        lib_test_runner.ok()
    else:
        lib_test_runner.fail()

