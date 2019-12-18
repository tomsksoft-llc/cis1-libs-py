#!/bin/bash

mkdir build
cd build

cp -r $cis_base_dir/jobs/$job_name/shared_srcs/lib-utils .
cp -r $cis_base_dir/jobs/$job_name/shared_srcs/tests .
cp lib-utils/lib_config.py.sample tests/lib_config.py

python3 -m pip install --user -r lib-utils/requirements.txt

cd tests

sed -i'' -e 's/PYTHON2 = \x27python\x27/PYTHON2 = \x27python2\x27/g; s/PYTHON3 = \x27python\x27/PYTHON3 = \x27python3\x27/g' lib_config.py

python3 lib_full_test.py

if [ $? -eq 0 ]
then
  echo "Tests finished successfully"
else
  echo "Tests failed"
  exit 1
fi

cd ..

cp lib-utils/* $cis_base_dir/jobs/$job_name/$build_number/artifacts

cd ..
