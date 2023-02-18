import click
from .py_libs import check_platform, execute
from .models import RaspberryPi3



@click.command()
@click.option('--build/--no-build', default=False)
@click.option('--test/--no-test', default=False)
@click.option('--git-clone/--no-git-clone', default=False)
@click.option('--make-iso/--no-make-iso', default=False)

def build(build):
    """Simple builder for RPI3"""
    if build:
        check_platform()
        print("BUILD WORLD")
        build_world = "make TARGET_ARCH=aarch64 SRCCONF=/dev/null __MAKE_CONF=/dev/null -j 4 buildworld"
        cd_src = "cd /usr/src"
        execute(f'{cd_src} && {build_world} >> /root/log_file.log')
    else:
        print("Nothing to build")    



if __name__ == '__main__':
    build()

