import sys

sys.path.append("../")
import lib_test_runner


def main():

    res = 0

    # invalid option argument
    if lib_test_runner.run(["../../lib-utils/redmine.py",
                            "--heRRRprp"], "must be ERROR ") == 0:
        res = 2

    # --help option
    if lib_test_runner.run(["../../lib-utils/redmine.py",
                            "--help"], "must be OK ") != 0:
        res = 2

    # Both invalid args
    if lib_test_runner.run(["../../lib-utils/redmine.py",
                            "issue", "-t"], "must be ERROR ") == 0:
        res = 2

    # Both invalid args
    if lib_test_runner.run(["../../lib-utils/redmine.py",
                            "issue", "-s"], "must be ERROR ") == 0:
        res = 2

    if res == 0:
        lib_test_runner.test_ok()
    else:
        lib_test_runner.test_fail()


if __name__ == "__main__":
    main()
