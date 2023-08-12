import logging
from . import execute
from datetime import datetime


log = logging.getLogger(__name__)

now = datetime.now()

current_time = now.strftime("%H:%M:%S")

def disk_unmount_dir(directory):
    print(f"Unmounting {directory}")
    # Use error-tolerant umount and rmdir
    subprocess.run(["umount", directory], stderr=subprocess.DEVNULL)
    subprocess.run(["rmdir", directory], stderr=subprocess.DEVNULL)

def disk_release_md(md):
    print(f"Releasing {md}")
    subprocess.run(["mdconfig", "-d", "-u", md], stderr=subprocess.DEVNULL)

_DISK_MDS = []  # List of MDs to clean up
_DISK_MOUNTED_DIRS = []  # List of directories to be unmounted when done

def disk_unmount_all():
    os.chdir(TOPDIR)
    for directory in _DISK_MOUNTED_DIRS:
        disk_unmount_dir(directory)
    _DISK_MOUNTED_DIRS.clear()
    for md in _DISK_MDS:
        disk_release_md(md)
    _DISK_MDS.clear()

def disk_record_mountdir(directory):
    _DISK_MOUNTED_DIRS.append(directory)

def disk_record_md(md):
    _DISK_MDS.append(md)

strategy_add(PHASE_UNMOUNT_LWW, disk_unmount_all)

def disk_create_image(image_path, size):
    size_display = f"{size // 1000000}MB"
    print(f"Creating a {size_display} raw disk image in:\n    {image_path}")
    if os.path.exists(image_path):
        os.remove(image_path)
    subprocess.run(["dd", "if=/dev/zero", f"of={image_path}", "bs=512", f"seek={size // 512}", "count=0"], stderr=subprocess.DEVNULL)

    disk_md = subprocess.run(["mdconfig", "-a", "-t", "vnode", "-f", image_path, "-x", "63", "-y", "255"], stdout=subprocess.PIPE, text=True, check=True).stdout.strip()
    disk_record_md(disk_md)

def disk_partition_mbr():
    print(f"Partitioning the raw disk image with MBR at {datetime.now()}")
    subprocess.run(["gpart", "create", "-s", "MBR", DISK_MD], stderr=subprocess.DEVNULL, check=True)

# Other functions in this section can be similarly translated
# ...

# Example usage of the above functions
# image_path = "/path/to/disk_image.img"
# image_size = 2000000000  # 2 GB
# disk_create_image(image_path, image_size)
# disk_partition_mbr()
