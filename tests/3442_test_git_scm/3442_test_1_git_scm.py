import sys

sys.path.append("../")
import lib_test_runner


def main():
    res = 0
    # --help usage check
    if lib_test_runner.run(["../../lib-utils/git_scm.py",
                            "--help"], "must be OK ") != 0:
        res = 2

        # Parameters usage check
    if lib_test_runner.run(["../../lib-utils/git_scm.py",
                            "TestDir"], "must be ERROR ") != 2:
        res = 2

    if res == 0:
        lib_test_runner.test_ok()
    else:
        lib_test_runner.test_fail()


if __name__ == "__main__":
    main()
