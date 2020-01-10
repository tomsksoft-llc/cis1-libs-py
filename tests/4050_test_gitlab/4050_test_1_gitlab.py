import sys

sys.path.append("../")
import lib_test_runner


def main():

    res = 0

    # invalid option argument
    if lib_test_runner.run(["../../lib-utils/gitlab.py",
                            "--heRRRprp"], "must be ERROR ") == 0:
        res = 2

    # --help option
    if lib_test_runner.run(["../../lib-utils/gitlab.py",
                            "--help"], "must be OK ") != 0:
        res = 2

    # One invalid arg
    if lib_test_runner.run(["../../lib-utils/gitlab.py",
                            "invalid"], "must be ERROR ") == 0:
        res = 2

    # --merge_request first invalid args
    if lib_test_runner.run(["../../lib-utils/gitlab.py",
                            "--merge_request"], "must be ERROR ") == 0:
        res = 2

    # --merge_request second invalid args
    if lib_test_runner.run(["../../lib-utils/gitlab.py",
                            "--merge_request", "source_branch"], "must be ERROR ") == 0:
        res = 2

    if res == 0:
        lib_test_runner.test_ok()
    else:
        lib_test_runner.test_fail()


if __name__ == "__main__":
    main()
