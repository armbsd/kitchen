import logging
import click
from .libs import check_platform, execute
from datetime import datetime


log = logging.getLogger(__name__)


def time_now() -> str:
    # datetime object containing current date and time
    now = datetime.now()
    
    # dd/mm/YY H:M:S
    return now.strftime("%d/%m/%Y %H:%M:%S")

def check_src():
    log.info("Found suitable FreeBSD source tree in: \n\t\t\t/usr/src")
    log.info("Found U-Boot port in: \n\t\t\t/usr/local/share/u-boot/u-boot-rpi3")
    log.info("Found firmware port in: \n\t\t\t/usr/local/share/rpi-firmware")


@click.command()
@click.option('--build/--no-build', default=False, help="Build source code.") 
@click.option('--test/--no-test', default=False, help="Test flag.")
@click.option('--git-clone/--no-git-clone', default=False, help="Clone src from FreeBSD git repo.")
@click.option('--make-image/--no-make-image', default=False, help="Make image.")

def main(build, test, git_clone, make_image):
    """Simple builder for RPI3"""
    log.info(f"Starting at {time_now()}.")
    check_src()
    if build:
        check_platform()
        print("BUILD WORLD")
        build_world = "make TARGET_ARCH=aarch64 SRCCONF=/dev/null __MAKE_CONF=/dev/null -j 4 buildworld"
        cd_src = "cd /usr/src"
        retcode, stdout, stderr = execute(f'{cd_src} && {build_world} >> /root/log_file.log')
        if retcode:
            log.error("Building is failed!")
            log.error(stderr)
        retcode, stdout, stderr = execute("make TARGET_ARCH=aarch64 SRCCONF=/dev/null __MAKE_CONF=/dev/null KERNCONF=GENERIC DESTDIR=/root/crochet/work/_.mount.freebsd installkernel")
        if retcode:
            log.error("Install kernel is failed!")
            log.error(stderr)
        
    if test:
        print('test') 
        

if __name__ == '__main__':
    main()

