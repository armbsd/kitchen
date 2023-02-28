import platform
import logging
import sys
from ..boards import RaspberryPi3, Board
from .executor import execute
from .disk import disk_create_image, disk_partition_mbr, disk_ufs_create, board_mount_all

log = logging.getLogger(__name__)

#
# Default implementations of board routines.
#

def check_platform():
    "Check platform on your build system"
    log.debug("Check your build platform...")
    if platform.system() != 'FreeBSD':
        log.error("System platform is not FreeBSD!")
        sys.exit(1)
    log.debug("Your build platform is OK!")

def board_generate_image_name (st: Board):
    "Generator of image name"
    log.debug("Generate board image name...")
    IMG=f'{st.WORK_DIR}/FreeBSD-{st.TARGET_ARCH}-{st.FREEBSD_MAJOR_VERSION}-{st.KERNCONF}-{st.BOARDNAME}.img'
    log.debug(f"Board image name: {IMG}")
    return IMG

def board_overlay_files (overlay, st:Board): 
    execute(f"cd {overlay}; find . | cpio -pmud {st.BOARD_FREEBSD_MOUNTPOINT}")

def board_default_create_image (st:Board):
    disk_create_image(board_generate_image_name(st), st.IMAGE_SIZE)

def board_default_partition_image ():
    "Default is to create a single UFS partition inside an MBR"
    disk_partition_mbr()
    disk_ufs_create()

def board_default_mount_partitions():
    board_mount_all()

def board_default_buildworld ( ):
    freebsd_buildworld()

def board_default_buildkernel ( ):
    freebsd_buildkernel()

def board_default_installworld (st:Board):
    freebsd_installworld(st)

def board_default_installkernel (st:Board):
    freebsd_installkernel(Board)

def board_default_goodbye (st:Board):
    print ("DONE.")
    print (f"Completed disk image is in: {board_generate_image_name(st)}")
    print ("")
    print ("Copy to a suitable memory card using a command such as:")
    print (f"dd if={board_generate_image_name(st)} of=/dev/da0 bs=1m")
    print ("(Replace /dev/da0 with the appropriate path for your card reader.)")
    print ("")

