import subprocess
import os
import sys



url = sys.argv[1]
depth = int(sys.argv[2])
external = sys.argv[3]
os.chdir('..')
process = subprocess.Popen('.\link_check.py {0} {1} {2}'.format(url,depth,external), stdout=subprocess.PIPE, shell=True)
output = process.communicate()
res = output[0].decode('utf8')
print(res)
    
