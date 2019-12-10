# Python Utility Library Development Guidelines for Continuous Integration Systems

Перед прочтением этого файла изучите 
Before proceeding with this file, first study [README.md](README.md)

The utilities source code must comply with http://google.github.io/styleguide/pyguide.html

The library contains a sample utility – util_sample.py, which can be used as a template. Please let us know If you find discrepancies between the sample utility and this documentation.

## Repository structure

`lib-utils` - contains all the utility files and their corresponding “spare components”. Everything in this directory comprises a utility library. To use it, simply copy this directory with all of its contents.

`tests` - stores the test scripts for each utility, and scripts that run these tests and generate a progress report. This is a service directory, which is not part of the library utilities.

`docs` - stores the documentation for developers of utility library.

Other directories and service files are not used by utilities.


## Utility Documentation

Each utility and all its additional .py files must be documented as follows:

1. The beginning of the file should contain the license information (this should be a copy of the library license).
2. The license information must list the author of the utility at the very end as shown in following example – util_sample.py.
3. The text of the license should be immediately followed by a description of the utility in the docstring format (see util_sample.py for reference).
4. All exported functions must be documented in compliance with CodeStyle (see above).
5. When starting the utility from the command line using the -h or --help command line options, the stdout must display the docstring of the use_as_os_command function that allows to use the utility as an OS command

Note: The utility test scripts are not part of the utility; and do not fall within the above requirements.

## Backward compatibility

Once in the library, the script is no longer allowed to change its interface and behavior. This is achieved by means of the following rules:
- each script is accompanied with the corresponding autotests (see below how they are designed and what they do)
- after autotests are added, they are never changed again, and they are run during the library building
Thus, any changes in the utility that trigger errors in the autotests are rejected.

When a new utility is added, a directory with tests is added along with it, which starts with a unique number for the entire library:

`tests/NNNN_test_<utilit yname>`

Where NNNN is the unique number. The directory contains the test scripts, which are named as follows:

`NNNN_test_N_<utlity name>.py`
 
Where N is the test ordinal number.
 
If successful, the test script should complete with return code 0. In case of error, the return code is NOT 0.
 
Use the following script to run all tests:

`tests/lib_full_test.py`

The `tests` directory acts as a process directory intended for their implementation.

When creating tests, you must use the following rules:
1. Each file should have only one test, unless the test logic dictates the opposite
2. The test is intended to ensure the script is run and executed as follows:
 
```python
import lib_test_runner
res = lib_test_runner.run(['../../lib-utils/<script name>', 'arg1',.. ], "Message for tests report")
```
 
3. The script should be completed using the following calls:
- in case the test is passed:

```python
lib_test_runner.test_ok()
```

• in case of error:

```python
lib_test_runner.test_fail()
```

Each utility must have tests that perform at least the following checks:
1. adequate response of the utility to the format of the command line parameters;
2. correct operation of the utility under adequate conditions;
3. adequate response of the utility to the function input parameters when it is used as a Python module.

## Local configuration

The library may require local settings in order to work in a specific installation. All these settings should be kept in the following file:

`lib_config.py`
 
which is stored outside the repository. The sample of this file stored in the repository:

`lib-utils/lib_config.py.sample`

For tests to run, the `lib_config.py` file is created in the `tests` directory.
 
## Library Repository Rules
 
A branch with the following name format is created for each new utility:
 
`NNNN_<utility name>`
 
NNNN is a unique number within the entire library.

The utility test scripts are developed along with it. The naming rules for script directory and scripts are described above.

Requirements to accept the utility:
1. Merge the latest master into the branch;
2. Bring the source code in line with the requirements listed above;
3. Check that all library tests are passed (this also applies to the new utility);
4. Generate the documentation using _TBD_;
5. Then submit a merge request.

Before merging the branches into master, the following actions are performed: library build, code review, verification of the compliance to this documentation, utility functional test, and utility compliance with the utility documentation. If all conditions and checks are completed and passed successfully, the branches are merged into the master.

## Rules for using third-party libraries

Third-party libraries are allowed. The license for third-party libraries should allow their unrestricted commercial and non-commercial use. All third-party license terms must be observed. All third-party libraries should be listed in the following file:

`lib-utils/requirements.txt`
 
The file format must comply with the following requirements:
 
 https://pip.pypa.io/en/stable/reference/pip_install/#requirements-file-format

## Library building

The building process (preparation of the package for distribution) comprises the following actions:
1. All tests are run on Windows, Linux, macOS/X; if at least one of them fails, the build is considered unsuccessful;
2. The full documentation in the HTML format is generated and checked manually in docs/ci-py-lib-reference.html;
3. The installation package is built.
