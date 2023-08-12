import subprocess
import shlex
import re
import time

def disk_partition_gpt(disk_md):
    print(f"Partitioning the raw disk image with EFI/GPT at {time.ctime()}")
    subprocess.run(["gpart", "create", "-s", "GPT", disk_md], check=True)

def gpt_add_fat_partition(disk_md, size):
    new_fat_slice = subprocess.run(["gpart", "add", "-b", "17m", "-s", size, "-t", "!EBD0A0A2-B9E5-4433-87C0-68B6B72699C7", "/dev/" + disk_md], text=True, capture_output=True, check=True).stdout.strip()
    new_fat_device = "/dev/" + new_fat_slice
    print(f"FAT partition is {new_fat_device}")
    subprocess.run(["newfs_msdos", new_fat_device], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    disk_created_new("FAT", new_fat_slice)

def gpt_add_ufs_partition(disk_md):
    new_ufs_slice = subprocess.run(["gpart", "add", "-t", "freebsd-ufs", "/dev/" + disk_md], text=True, capture_output=True, check=True).stdout.strip()
    new_ufs_device = "/dev/" + new_ufs_slice
    print(f"UFS partition is {new_ufs_device}")
    subprocess.run(["newfs", new_ufs_device], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    disk_created_new("UFS", new_ufs_slice)

# Assuming you have a function disk_created_new for handling new partitions
def disk_created_new(partition_type, partition_slice):
    print(f"New {partition_type} partition created: {partition_slice}")