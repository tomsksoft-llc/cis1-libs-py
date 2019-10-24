from typing import List
import subprocess
import sys

import lib_config


OK = 'OK'
ERR = 'FAIL'


def run(args: List[str], msg: str = None):
    args = [ lib_config.PYTHON3 ] + args;
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    code = proc.returncode
    proc.terminate()
    args_str = ' '.join(args)
    if code:
        print(f"{args_str:.<30}{msg:.^30}{ERR:.>10}")
        print(stdout.decode('utf-8'))
        print(stderr.decode('utf-8'))
    else:
        print(f"{args_str:.<30}{msg:.^30}{OK:.>10}")
    return code


def ok():
    sys.exit(0)


def fail():
    sys.exit(1)
