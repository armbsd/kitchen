import subprocess
import os

def scm_update_sourcetree(freebsd_src, workdir):
    print(f"Updating source tree {freebsd_src}")
    os.chdir(freebsd_src)
    
    if os.path.exists('.git'):
        subprocess.run(['git', 'pull'], stdout=open(os.path.join(workdir, '_.gitpull.log'), 'w'), check=True)
    elif os.path.exists('.hg'):
        subprocess.run(['hg', 'pull', '-u'], stdout=open(os.path.join(workdir, '_.hgpull.log'), 'w'), check=True)
    elif shutil.which('svn'):
        subprocess.run(['svn', 'update'], stdout=open(os.path.join(workdir, '_.svnupdate.log'), 'w'), check=True)
    else:
        subprocess.run(['svnlite', 'update'], stdout=open(os.path.join(workdir, '_.svnupdate.log'), 'w'), check=True)
    
    os.chdir(workdir)

def scm_get_revision(freebsd_src):
    _PWD = os.getcwd()
    os.chdir(freebsd_src)
    source_version = None
    
    if os.path.exists('.git'):
        try:
            source_version = subprocess.run(['git', 'rev-parse', '--verify', '--short', 'HEAD'], text=True, capture_output=True, check=True).stdout.strip()
        except subprocess.CalledProcessError:
            print(f"Warning: {freebsd_src} appears to be a git checkout, but 'git rev-parse' is not giving us a commit ID")
            source_version = "git-rUNKNOWN"
    elif os.path.exists('.hg'):
        try:
            source_version = subprocess.run(['hg', 'id', '-i'], text=True, capture_output=True, check=True).stdout.strip()
        except subprocess.CalledProcessError:
            print(f"Warning: {freebsd_src} appears to be a mercurial checkout, but 'hg id' is not giving us a commit ID")
            source_version = "hg-rUNKNOWN"
    elif os.path.exists('.svn'):
        try:
            source_version = subprocess.run(['svnversion', freebsd_src], text=True, capture_output=True, check=True).stdout.strip().replace(":", "_")
        except subprocess.CalledProcessError:
            try:
                source_version = subprocess.run(['svnliteversion', freebsd_src], text=True, capture_output=True, check=True).stdout.strip().replace(":", "_")
            except subprocess.CalledProcessError:
                print(f"Warning: {freebsd_src} appears to be a subversion checkout, but 'svnversion' is not giving us a revision ID")
                source_version = "svn-rUNKNOWN"
    
    os.chdir(_PWD)
    print(f"Source version is: {source_version if source_version else 'unknown'}")
    return source_version

# Assuming you have defined the necessary variables like FREEBSD_SRC, WORKDIR
# scm_update_sourcetree(FREEBSD_SRC, WORKDIR)
# source_version = scm_get_revision(FREEBSD_SRC)