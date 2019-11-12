import sys
import subprocess
import pathlib
import re
import os

import lib_config

OK = 'OK'
ERR = 'FAIL'

def run_test(d, f):
    proc = subprocess.Popen([lib_config.PYTHON3, f.name], cwd=d, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=os.environ)
    stdout, stderr = proc.communicate()
    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')
    status = proc.poll()
    if  status == 0:
        print(f"{OK:.<10}{f.name:.>30}")
    else:
        print(f"{ERR:.<10}{f.name:.>30}")
        print("---------------------------------------------------------------")
        print(stdout)
        print(stderr)
        print("---------------------------------------------------------------")
        print()
    proc.terminate()
    return status


def run_all_tests():
    os.environ['PYTHONPATH'] = '..;../../lib-utils'

    print("\nCI Python scripts lib self testing started:\n")
    f = open("test_lib_full_test.py")
    if run_test(".", f) != 0:
        print("FATAL...........test_runner self check failed.\nExecution aborted\n\n")
        sys.exit(3)
    print("\nTests runner self test passed, starting lib scripts tests:\n")
    
    status = 0;
    for d in pathlib.Path('./').iterdir():
        if not d.is_dir(): continue
        m = re.match(r"\d+_test_(?P<test_name>[\w_]+)", d.name)
        if m is None: continue
        for f in d.iterdir():
            if not f.is_file(): continue
            if not f.name[-3:] == '.py': continue
            if f.name == '__init__.py': continue
            if run_test(d, f) != 0:
                status = 2
    if status == 0:
        print("\nAll tests passed successfully")
    else:
        print("\nThere are error(s) in the some test(s). See log for details.\n\nLibrary testing FAILED\n\n")
    sys.exit(status)


if __name__ == '__main__':
    run_all_tests()
