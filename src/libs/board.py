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

# Default implementations of board routines.

# Boards that need more than this can define their own.
def board_mountpoint_defaults():
    global BOARD_UFS_MOUNTPOINT_PREFIX, BOARD_FREEBSD_MOUNTPOINT_PREFIX, BOARD_FAT_MOUNTPOINT_PREFIX, BOARD_BOOT_MOUNTPOINT_PREFIX
    if not BOARD_UFS_MOUNTPOINT_PREFIX:
        BOARD_UFS_MOUNTPOINT_PREFIX = f"{WORKDIR}/_.mount.ufs"
    if not BOARD_FREEBSD_MOUNTPOINT_PREFIX:
        BOARD_FREEBSD_MOUNTPOINT_PREFIX = f"{WORKDIR}/_.mount.freebsd"
    if not BOARD_FAT_MOUNTPOINT_PREFIX:
        BOARD_FAT_MOUNTPOINT_PREFIX = f"{WORKDIR}/_.mount.fat"
    if not BOARD_BOOT_MOUNTPOINT_PREFIX:
        BOARD_BOOT_MOUNTPOINT_PREFIX = f"{WORKDIR}/_.mount.boot"

# Default is to install world ...
FREEBSD_INSTALL_WORLD = True

# List of all board dirs.
BOARDDIRS = []

# the board's name, later to be used in IMGNAMe
BOARDNAME = ""

# $1: name of board directory
def board_setup(board_name):
    global BOARDDIRS, BOARDNAME
    BOARDDIR = f"{TOPDIR}/board/{board_name}"
    BOARDNAME = board_name
    if not os.path.exists(f"{BOARDDIR}/setup.sh"):
        print(f"Can't setup board {board_name}.")
        print(f"No setup.sh in {BOARDDIR}.")
        exit(1)
    BOARDDIRS.append(BOARDDIR)
    print(f"Board: {board_name}")
    exec(open(f"{BOARDDIR}/setup.sh").read())
    PRIORITY = 20
    strategy_add(PHASE_FREEBSD_BOARD_INSTALL, board_overlay_files, BOARDDIR)
    BOARDDIR = None

def board_generate_image_name():
    global IMG
    if not IMGDIR:
        _IMGDIR = WORKDIR
    else:
        _IMGDIR = IMGDIR
    if IMGNAME:
        eval(f"IMG = {_IMGDIR}/{IMGNAME}")
    if not IMG:
        if not SOURCE_VERSION:
            IMG = f"{_IMGDIR}/FreeBSD-{TARGET_ARCH}-{FREEBSD_MAJOR_VERSION}-{KERNCONF}-{BOARDNAME}.img"
        else:
            IMG = f"{_IMGDIR}/FreeBSD-{TARGET_ARCH}-{FREEBSD_VERSION}-{KERNCONF}-{SOURCE_VERSION}-{BOARDNAME}.img"
    print("Image name is:")
    print(f"    {IMG}")

# Run this late, so we print the image name after other post-config has had a chance
PRIORITY = 200
strategy_add(PHASE_POST_CONFIG, board_generate_image_name)

# $1 - BOARDDIR
# Registered from the end of board_setup so that it can get the BOARDDIR
# as an argument. (There are rare cases where we actually load
# more than one board definition; in those cases, this will get
# registered and run once for each BOARDDIR.)
# TODO: Are there other examples of this kind of thing?
# If so, is there a better mechanism?
def board_overlay_files(BOARDDIR):
    if os.path.isdir(f"{BOARDDIR}/overlay"):
        print(f"Overlaying board-specific files from {BOARDDIR}/overlay")
        subprocess.run(["cd", f"{BOARDDIR}/overlay", "&&", "find", ".", "|", "cpio", "-pmud", BOARD_FREEBSD_MOUNTPOINT], shell=True, check=True)

def board_defined():
    if not BOARDDIRS:
        print("No board setup?")
        print(f"Make sure a suitable board_setup command appears at the top of {CONFIGFILE}")
        exit(1)

strategy_add(PHASE_POST_CONFIG, board_defined)

# TODO: Not every board requires -CURRENT; copy this into all the
# board setups and remove it from here.
strategy_add(PHASE_CHECK, freebsd_current_test)

def board_check_image_size_set():
    # Check that IMAGE_SIZE is set.
    if not IMAGE_SIZE:
        print("Error: $IMAGE_SIZE not set.")
        exit(1)

strategy_add(PHASE_CHECK, board_check_image_size_set)

def board_default_create_image():
    disk_create_image(IMG, IMAGE_SIZE)

strategy_add(PHASE_IMAGE_BUILD_LWW, board_default_create_image)

# Default is to create a single UFS partition inside an MBR
def board_default_partition_image():
    disk_partition_mbr()
    disk_ufs_create()

strategy_add(PHASE_PARTITION_LWW, board_default_partition_image)

# Default mounts all the FreeBSD partitions
def board_default_mount_partitions():
    board_mount_all()

strategy_add(PHASE_MOUNT_LWW, board_default_mount_partitions)

def board_default_buildworld():
    freebsd_buildworld()

strategy_add(PHASE_BUILD_WORLD, board_default_buildworld)

def board_default_buildkernel():
    freebsd_buildkernel()

strategy_add(PHASE_BUILD_KERNEL, board_default_buildkernel)

def board_default_installworld():
    if FREEBSD_INSTALL_WORLD:
        freebsd_installworld(BOARD_FREEBSD_MOUNTPOINT)

strategy_add(PHASE_FREEBSD_INSTALLWORLD_LWW, board_default_installworld)

def board_default_installkernel():
    freebsd_installkernel()

# Note: we don't automatically put installkernel into the
# strategy here because different boards install the kernel
# into different places (e.g., separate firmware or
# separate partition).

def board_default_goodbye():
    print("DONE.")
    print(f"Completed disk image is in: {IMG}")
    print()
    print("Copy to a suitable memory card using a command such as:")
    print(f"dd if={IMG} of=/dev/da0 bs=1m")