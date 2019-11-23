import sys

sys.path.append("../")
import lib_test_runner


def main():
    error = None
    # --help usage check
    res = lib_test_runner.run(["../../lib-utils/git_scm.py",
                               "--help"], "--help check ")
    if res != 0:
        error = True

    # Parameters usage check
    res = lib_test_runner.run(["../../lib-utils/git_scm.py",
                               "TestDir"], "Check without repository url ")
    if res != 2:
        error = True
    if not error:
        lib_test_runner.test_ok()
    else:
        lib_test_runner.test_fail()


if __name__ == "__main__":
    main()
