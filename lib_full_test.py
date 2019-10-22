import subprocess
import pathlib
import re
import os

import lib_config

OK = 'OK'
ERR = 'FAIL'


def run_tests():
    os.environ['PYTHONPATH'] = '..'
    for d in pathlib.Path('./').iterdir():
        if not d.is_dir(): continue
        m = re.match(r"\d+_test_(?P<test_name>[\w_]+)", d.name)
        if m is None: continue
        print(f"Tesing {d.name}")
        for f in d.iterdir():
            if not f.is_file(): continue
            if not f.name[-3:] == '.py': continue
            if f.name == '__init__.py': continue

            proc = subprocess.Popen([lib_config.PYTHON3, f.name], cwd=d, stdout=subprocess.PIPE, env=os.environ)
            stdout, stderr = proc.communicate()
            stdout = stdout.decode('utf-8')
            lines = stdout.split('\n')
            last_msg = lines[-2]
            if proc.poll() == 0:
                print(f"{f.name:.<30}{last_msg:.^30}{OK:.>10}")
            else:
                print(f"{f.name:.<30}{last_msg:.^30}{ERR:.>10}")
                print('\n'.join(lines))
            proc.terminate()
        print()


if __name__ == '__main__':
    run_tests()
