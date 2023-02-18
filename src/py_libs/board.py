import platform
import logging
import sys
from ..models import RaspberryPi3

log = logging.getLogger(__name__)

def board_mountpoint_defaults():
    print ("Hello board_mountpoint_defaults ")


def  board_setup ():
    pass

def  check_platform():
        if platform.system() != 'FreeBSD':
            log.error("System platform is not FreeBSD!")
            sys.exit(1)


def board_generate_image_name (st: RaspberryPi3):
    IMG=f'{st.IMGDIR}/FreeBSD-{st.TARGET_ARCH}-{st.FREEBSD_MAJOR_VERSION}-{st.KERNCONF}-{st.BOARDNAME}.img'
    return IMG