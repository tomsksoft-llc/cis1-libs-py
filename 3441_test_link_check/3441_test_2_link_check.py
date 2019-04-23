import subprocess
import os
import sys
url = 'https://github.com/tomsksoft-llc/cis1-libs-py'
depth = 2
external = 'True'
os.chdir('..')
process = subprocess.Popen('.\link_check.py {0} {1} {2}'.format(url,depth,external), stdout=subprocess.PIPE, shell=True)
output = process.communicate()
res = output[0].decode('utf8')
print(res)
    
