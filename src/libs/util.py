import fileinput
import shutil

def util_add_passwd(line_to_add):
    with fileinput.input("etc/master.passwd", inplace=True) as f:
        for line in f:
            if not line.startswith(line_to_add.split(':')[0] + ':'):
                print(line, end='')
        print(line_to_add)
    
    shutil.copy("etc/master.passwd", "etc/master.passwd.new")
    shutil.move("etc/master.passwd.new", "etc/master.passwd")
    subprocess.run(["pwd_mkdb", "-p", "-d", f"{os.getcwd()}/etc", "etc/master.passwd"], check=True)

def util_add_user_group(user, group):
    with fileinput.input("etc/group", inplace=True) as f:
        for line in f:
            if line.startswith(group + ":"):
                line = line.rstrip('\n') + ',' + user + '\n'
            print(line, end='')

# Example usage
# util_add_passwd("root:<passwd>:0:0::0:0:Charlie &:/root:/bin/csh")
# util_add_user_group("me", "wheel")