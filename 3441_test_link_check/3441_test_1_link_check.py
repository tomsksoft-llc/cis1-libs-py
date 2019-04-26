import subprocess
import os
import sys



url = 'http://tomsksoft.ru/'
depth = 0
external = 'True'
os.chdir('..')
process = subprocess.Popen('.\link_check.py {0} {1} {2}'.format(url,depth,external), stdout=subprocess.PIPE, shell=True)
output = process.communicate()
res = output[0].decode('utf8')
code = process.poll()
print('Result: \n',res)
print('Code: ',code)
if 'usage:' in res:
    usage = True
else:
    usage = False

print('Is usage = ', usage)
    
