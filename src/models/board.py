from dataclasses import dataclass

@dataclass
class Board:

    PREFIX="/usr/local"
    SHARE_PATH=f"{PREFIX}/share"

    # This should be overridden by the board setup
    TARGET_ARCH: str = ''

    # Board setup should not touch these, so users can
    FREEBSD_OBJ = '/usr/obj'
    FREEBSD_SRC = '/usr/src'
    FREEBSD_EXTRA_ARGS = []
    FREEBSD_WORLD_EXTRA_ARGS = []
    FREEBSD_BUILDWORLD_EXTRA_ARGS = []
    FREEBSD_INSTALLWORLD_EXTRA_ARGS = []
    FREEBSD_KERNEL_EXTRA_ARGS = []
    FREEBSD_BUILDKERNEL_EXTRA_ARGS = []
    FREEBSD_INSTALLKERNEL_EXTRA_ARGS = []

    # Make non-empty to override the usual build-avoidance
    FREEBSD_FORCE_BUILDKERNEL: str = ''
    FREEBSD_FORCE_BUILDWORLD: str = ''

    # Hooks for board setup
    FREEBSD_WORLD_BOARD_ARGS = []
    FREEBSD_BUILDWORLD_BOARD_ARGS = []
    FREEBSD_INSTALLWORLD_BOARD_ARGS = []
    FREEBSD_KERNEL_BOARD_ARGS = []
    FREEBSD_BUILDKERNEL_BOARD_ARGS = []
    FREEBSD_INSTALLKERNEL_BOARD_ARGS = []


    SHARE_PATH: str = ''
    TARGET_ARCH: str = ''
    TARGET: str = ''
    KERNCONF: str = ''
    UBOOT_PORT: str = ''
    UBOOT_BIN: str = ''
    FIRMWARE_PORT: str = ''
    FIRMWARE_BIN: str = ''
    FIRMWARE_FILES = []
    FIRMWARE_PATH: str = ''
    UBOOT_PATH: str = ''

