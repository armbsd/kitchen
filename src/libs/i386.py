import subprocess
import shlex
import os

def clean_old_boot_bits(workdir):
    boot_dir = os.path.join(workdir, "boot")
    if os.path.exists(boot_dir):
        subprocess.run(["rm", "-rf", boot_dir], check=True)
    os.makedirs(os.path.join(boot_dir, "defaults"), exist_ok=True)

def generic_i386_build_mbr(freebsd_src, target_arch, workdir):
    print("Building MBR")
    buildenv = subprocess.run(["make", "-C", freebsd_src, f"TARGET_ARCH={target_arch}", "buildenvvars"], text=True, capture_output=True, check=True).stdout.strip()
    mbr_dir = os.path.join(freebsd_src, "stand/i386/mbr")
    subprocess.run(["make", "-C", mbr_dir], env=shlex.split(buildenv), stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    install_cmd = f"{buildenv} make DESTDIR={workdir} install"
    if subprocess.run(install_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode != 0:
        print("Failed to build MBR:")
        print(subprocess.run(["tail", os.path.join(workdir, "_.i386.mbr.log")], text=True, capture_output=True).stdout)
        exit(1)

def generic_i386_build_boot2(freebsd_src, target_arch, workdir):
    print("Building Boot2")
    buildenv = subprocess.run(["make", "-C", freebsd_src, f"TARGET_ARCH={target_arch}", "buildenvvars"], text=True, capture_output=True, check=True).stdout.strip()
    boot2_dir = os.path.join(freebsd_src, "stand/i386/boot2")
    subprocess.run(["make", "-C", boot2_dir], env=shlex.split(buildenv), stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    install_cmd = f"{buildenv} make DESTDIR={workdir} install"
    if subprocess.run(install_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode != 0:
        print("Failed to build boot2:")
        print(subprocess.run(["tail", os.path.join(workdir, "_.i386.boot2.log")], text=True, capture_output=True).stdout)
        exit(1)

def generic_i386_build_loader(freebsd_src, target_arch, workdir):
    print("Building Loader")
    buildenv = subprocess.run(["make", f"TARGET_ARCH={target_arch}", "buildenvvars"], text=True, capture_output=True, check=True).stdout.strip()
    loader_dir = os.path.join(freebsd_src, "stand/i386/loader")
    makesyspath = os.path.join(freebsd_src, "share/mk")
    os.environ["MAKESYSPATH"] = makesyspath
    subprocess.run(["make", "-C", loader_dir], env=shlex.split(buildenv), stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    
    install_cmd = f"{buildenv} make DESTDIR={workdir} MK_MAN=no install"
    if subprocess.run(install_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode != 0:
        print("Failed to copy i386 loader into WORKDIR:")
        print(subprocess.run(["tail", os.path.join(workdir, "_.i386_loader_install.log")], text=True, capture_output=True).stdout)
        exit(1)

# Assuming you have disk_partition_mbr, disk_ufs_create, and disk_ufs_slice functions defined
def generic_i386_partition_image(disk_md, workdir):
    disk_partition_mbr(disk_md)
    disk_ufs_create(workdir)
    print("Installing bootblocks")
    subprocess.run(["gpart", "bootcode", "-b", os.path.join(workdir, "boot/mbr"), disk_md], check=True)
    subprocess.run(["gpart", "set", "-a", "active", "-i", "1", disk_md], check=True)
    subprocess.run(["bsdlabel", "-B", "-b", os.path.join(workdir, "boot/boot"), disk_ufs_slice()], check=True)

# Assuming you have defined the necessary variables like FREEBSD_SRC, TARGET_ARCH, PHASE_BUILD_OTHER, PHASE_PARTITION_LWW
strategy_add = lambda phase, function: None  # Placeholder for strategy_add

# Call the functions with appropriate arguments
# clean_old_boot_bits(WORKDIR)
# generic_i386_build_mbr(FREEBSD_SRC, TARGET_ARCH, WORKDIR)
# generic_i386_build_boot2(FREEBSD_SRC, TARGET_ARCH, WORKDIR)
# generic_i386_build_loader(FREEBSD_SRC, TARGET_ARCH, WORKDIR)
# generic_i386_partition_image(DISK_MD, WORKDIR)