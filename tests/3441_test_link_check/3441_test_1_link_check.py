import sys
import lib_test_runner

# Run program and return code
def main():
    res = 0
    
    # Depth usage check
    if lib_test_runner.run(["../../lib-utils/link_check.py", "https://deskroll.com/",
                            "0", "False"], "must be ERROR ") != 2:

        res = 2
        
    # External usage check
    if lib_test_runner.run(["../../lib-utils/link_check.py", "https://deskroll.com/",
                            "1", "Folse"], "must be ERROR ") != 2:
        res = 2
    # --help option
    if lib_test_runner.run(["../../lib-utils/link_check.py",
                            "--help"], "must be OK ") != 0:
        res = 2        
    # Parameters usage check
    if lib_test_runner.run(["../../lib-utils/link_check.py"],
                             "must be ERROR ") != 2:
        res = 2     
    if res == 0:
        lib_test_runner.test_ok()
    else:
        lib_test_runner.test_fail()
if '__main__':
    main()

