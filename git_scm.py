import sys
import subprocess
import os

def repo(rep, commit_id, ref, dir, mod_h, mod_b):
    FNULL = open(os.devnull, 'w')
    if mod_b: 
        subprocess.run('git clone {0} -b {1} {2}'.format(rep,ref,dir))
    else:
        subprocess.run('git clone {0} {1}'.format(rep,dir))
    
    os.chdir(dir)
    subprocess.run('git rev-parse --is-inside-work-tree', stdout=FNULL)
    
    if not mod_h:
        process = subprocess.Popen('git rev-parse --verify HEAD', stdout=subprocess.PIPE, shell=True)
        output = process.communicate()
        commit_id = output[0].decode('utf8')
        commit_id = commit_id[:-2]

        
    
    subprocess.run('git reset --hard', stdout=FNULL)
    subprocess.run('git clean -fdx', stdout=FNULL)
    subprocess.run('git fetch --tags --progress {0} +refs/heads/*:refs/remotes/origin/*'.format(rep), stdout=FNULL)
    subprocess.run('git rev-parse {0}'.format(commit_id), stdout=FNULL)
    subprocess.run('git config core.sparsecheckout', stdout=FNULL)
    subprocess.run('git checkout -f {0}'.format(commit_id), stdout=FNULL)
    #subprocess.run('git rev-list {0}'.format(commit_id))
    return 0
    
def usage():
    print("""
usage:

git_scm <repo> [-b branch]|[-h commit_hash]<dir>

by default get (pull and checkout) HEAD of the master branch from repo

-b bransh - get head of the specified branch
-h commit_hash - get the specified revision

Return value:

0 - if success
non zero - if any error
""")
if '__main__':
    #repo(sys.argv[1], sys.argv[2], '', sys.argv[3])
    if sys.argv[1] == '--help':
        usage()
    else:
        mod_h, mod_b,commit_id,ref = False, False, False, False
        for arg in range(len(sys.argv)):
            if sys.argv[arg] == '-h':
                mod_h = True
                commit_id = sys.argv[arg+1]
                sys.argv[arg+1] = None
            if sys.argv[arg] == '-b':
                mod_b = True
                ref = sys.argv[arg+1]
                sys.argv[arg+1] = None

        rep = sys.argv[1]
        dir = sys.argv[-1:]
        dir = dir[0]
        
        try:
            if dir is None:
                raise Exception("fatal:the last argument should be <dir>")
            
            res = repo(rep, commit_id, ref, dir, mod_h, mod_b)
            print(res)
        except Exception as err:
            print(err)
            usage()
            
            
            
            
            
                
        

