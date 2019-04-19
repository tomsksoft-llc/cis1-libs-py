import sys
import subprocess
import os

def repo(rep, commit_id, ref, dir):
    FNULL = open(os.devnull, 'w')
    if ref != '':
        
        subprocess.run('git clone {0} -b {1} {2}'.format(rep,ref,dir))
    else:
        print('gogo')
        subprocess.run('git clone {0} {1}'.format(rep,dir))
    
    os.chdir(dir)
    subprocess.run('git rev-parse --is-inside-work-tree')
    
    if commit_id == '':
        process = subprocess.Popen('git rev-parse --verify HEAD', stdout=subprocess.PIPE, shell=True)
        output = process.communicate()
        commit_id = output[0].decode('utf8')
        commit_id = commit_id[:-2]

        
    
    subprocess.run('git reset --hard')
    subprocess.run('git clean -fdx')
    subprocess.run('git fetch --tags --progress {0} +refs/heads/*:refs/remotes/origin/*'.format(rep))
    subprocess.run('git rev-parse {0}'.format(commit_id))
    subprocess.run('git config core.sparsecheckout')
    subprocess.run('git checkout -f {0}'.format(commit_id))
    subprocess.run('git rev-list {0}'.format(commit_id))
    return True

if '__main__':
    repo(sys.argv[1], sys.argv[2], '', sys.argv[3])
    """
    if sys.argv[1] == '--help':
        print('''
usage:      <-b>  <ref>  <commit_id> <dir>   
            <link>[<args>]<dir>
            
    -b                  Download repository on branch
    <ref>               Branch name
    <commit_id>         Commit's id(hash)
    <dir>               The directory in which the repository will be installed (required) 
        ''')


    try:
        repo = sys.argv[1]
        if sys.argv[2] == '-b':
            mode = '-b'

            try:
                ref = sys.argv[3]
                dir = sys.argv[4]
                clone_ref(repo,'', ref, dir)
            except:
                print ('fatal:directory or branch not specified')

        else:
            commit_id = sys.argv[2]
            dir = sys.argv[3]
            clone_repo(repo, commit_id,'', dir)

    except:
        try:
            repo = sys.argv[1]
            dir = sys.argv[2]
            clone_repo(repo,'','',dir)
        except:
            print('''
usage:      [-b]  <ref>  <commit_id> <dir>   
            <link>[<args>]<dir>

--help to learn more
                
        ''')
"""



#af696919d867d9d55e618d3307dc6293baa2fb2b
