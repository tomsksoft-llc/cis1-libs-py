# ci-py-lib

CI Python utilities library for CI purposes

This library contains a set of Python utilities designed for Continuous Integration systems.

## Library usage

Each utility is a separate .py file. Each of them can be used in two ways:

1. as an OS command, in which case the parameters are transmitted through the command line, the return code 0 means successful execution, not 0 - an error. The Stdout/stderr must be updated with information on the status of implementation and error diagnostics sufficient to debug the program that uses this utility. The function that is used to run the utility in this mode must be called use_as_os_command; it must parse the command line within itself and perform the necessary actions;

2. as a python module, the call function name matches the name of the script, but there may be other functions, and, in such case, they should be documented inside the module itself (see below). The key function should return 0 if successful, not 0 – in case of error. Functions located inside the utility, but not intended for external calls, must remain local. Diagnosis of effort conditions must be informative enough to enable error diagnostics based on the key function return code (and additional functions if necessary)

All utilities are stored in the lib-utils repository directory. In order to use them, simply clone the master branch, and set up the configuration in the `lib-utils/lib_config.py` file, an example of which can be found in `lib-utils/lib_config.py.sample`.

The utility documentation is stored in it, and can be obtained both from the command line and using Pydoc:

For information on how to use the utility from the command line:
```console
$ python <util_name>.py -h | --help
```

Full utility documentation:
```
$ python pydoc.py  ./<util_name>.py
```

The documentation for all utilities is stored in the [lib-utils/py-lib-guide.html](lib-utils/py-lib-guide.html).

## Additional Information

• Each utility is tested while building using test scripts stored in this repository. The scripts are not part of the utilities.
• The library supports backward compatibility at least within a major version.
• The library is cross-platform.
• Instructions for library developers are located in the [docs/devguide.md](docs/devguide.md) file of this repository.
