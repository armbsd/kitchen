from dataclasses import dataclass
from . import Board

@dataclass
class RaspberryPi3(Board):
    PREFIX="/usr/local"
    SHARE_PATH=f"{PREFIX}/share"
    TARGET_ARCH = 'aarch64'
    TARGET = 'aarch64'
    KERNCONF = 'GENERIC'
    UBOOT_PORT = 'u-boot-rpi3'
    UBOOT_BIN = 'u-boot.bin'
    FIRMWARE_PORT = 'rpi-firmware'
    FIRMWARE_BIN = 'bootcode.bin'
    FIRMWARE_FILES = ['bootcode.bin', 
        'fixup.dat', 'fixup_cd.dat', 'fixup_db.dat', 'fixup_x.dat',
        "start.elf", "start_cd.elf", "start_db.elf", "start_x.elf", "armstub8.bin"]
    FIRMWARE_PATH = f"{SHARE_PATH}/{FIRMWARE_PORT}"
    UBOOT_PATH = f"{SHARE_PATH}/u-boot/{UBOOT_PORT}"
    IMAGE_SIZE = 3 * 1000 * 1000 * 1000
    IMGDIR =  "/root/work"
    # FIXME get branch name from source:  git rev-parse --abbrev-ref HEAD 
    FREEBSD_MAJOR_VERSION = 'stable-12'
    BOARDNAME = "RaspberryPi3"
