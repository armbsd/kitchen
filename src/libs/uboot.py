import os
import subprocess

def _uboot_download_instructions(uboot_src_var, *commands):
    _UBOOT_SRC_VAR = uboot_src_var
    _UBOOT_SRC = os.environ[_UBOOT_SRC_VAR]
    print()
    print("Expected to see U-Boot sources in")
    print(f"    {_UBOOT_SRC}")
    print("Use the following command to get the U-Boot sources")
    print()

    if not commands:
        UBOOT_VERSION = uboot_version_from_dir(_UBOOT_SRC)
        
        if UBOOT_VERSION == "unknown":
            UBOOT_VERSION = os.environ["UBOOT_PATCH_VERSION"]
        
        if UBOOT_VERSION == "master":
            print("git clone git://git.denx.de/projects/u-boot.git u-boot-master")
        else:
            print(f"ftp ftp://ftp.denx.de/pub/u-boot/u-boot-{UBOOT_VERSION}.tar.bz2")
            print(f"tar xf u-boot-{UBOOT_VERSION}.tar.bz2")
    else:
        for command in commands:
            print(f" $ {command}")

    print()
    print(f"Edit ${_UBOOT_SRC_VAR} in config.sh if you want the sources in a different directory.")
    print("Run this script again after you have the U-Boot sources installed.")
    exit(1)

def uboot_test(uboot_src_var, *commands):
    # Assuming you have defined the necessary variables like UBOOT_PATCH_VERSION
    _uboot_check_patch_version()

    if shutil.which("gmake") is None:
        print("U-Boot build requires 'gmake'")
        print("Please install devel/gmake and re-run this script.")
        exit(1)
    
    if shutil.which("gsed") is None:
        print("U-Boot build requires 'gsed'")
        print("Please install textproc/gsed and re-run this script.")
        exit(1)
    
    uboot_src = os.environ[uboot_src_var]
    if os.path.isfile(uboot_src):
        print(f"Found U-Boot sources in:\n    {uboot_src}")
    else:
        _uboot_download_instructions(uboot_src_var, *commands)

def uboot_patch(uboot_src, *patch_files):
    _UBOOT_SRC = uboot_src
    print(" ".join(patch_files), file=open(os.path.join(_UBOOT_SRC, "_.uboot.to.be.patched"), "w"))

    if os.path.isfile(os.path.join(_UBOOT_SRC, "_.uboot.patched")):
        if filecmp.cmp(os.path.join(_UBOOT_SRC, "_.uboot.patched"), os.path.join(_UBOOT_SRC, "_.uboot.to.be.patched")):
            os.remove(os.path.join(_UBOOT_SRC, "_.uboot.to.be.patched"))
            return 0
        else:
            print("U-Boot sources have already been patched, but with the wrong patches.")
            print("Please check out fresh U-Boot sources and try again.")
            exit(1)
    
    if os.path.isfile(os.path.join(_UBOOT_SRC, "_.uboot.patched")):
        open(os.path.join(_UBOOT_SRC, "_.uboot.patched"), "w").close()
        return 0
    
    os.chdir(_UBOOT_SRC)
    print(f"Patching U-Boot at {datetime.datetime.now()}")
    print(f"    (Logging to {_UBOOT_SRC}/_.uboot.patch.log)")
    
    if os.path.exists(patch_files[0]):
        for patch_file in patch_files:
            print(f"   Applying patch {patch_file}")
            with open(patch_file, "rb") as f:
                patch_data = f.read()
            p = subprocess.Popen(["patch", "-N", "-p1"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = p.communicate(input=patch_data)
            
            if p.returncode == 0:
                print("Patched successfully")
            else:
                print(f"Patch didn't apply: {patch_file}")
                print(f"  Log in {_UBOOT_SRC}/_.uboot.patch.log")
                exit(1)
    else:
        print("   No patches found; skipping")
    
    open(os.path.join(_UBOOT_SRC, "_.uboot.to.be.patched"), "w").close()
    os.rename(os.path.join(_UBOOT_SRC, "_.uboot.to.be.patched"), os.path.join(_UBOOT_SRC, "_.uboot.patched"))

def uboot_configure(uboot_src, configuration):
    print(configuration, file=open(os.path.join(uboot_src, "_.uboot.to.be.configured"), "w"))

    if os.path.isfile(os.path.join(uboot_src, "_.uboot.configured")):
        return 0

    os.chdir(uboot_src)
    print(f"Configuring U-Boot at {datetime.datetime.now()}")
    print(f"    (Logging to {uboot_src}/_.uboot.configure.log)")
    
    # U-Boot 2014.10 chokes when csh sets VENDOR; fixed in U-Boot 2015.01
    # This can be removed when U-Boot 2014.10 is ancient history.
    os.environ.pop("VENDOR", None)
    gmake_cmd = ["gmake", "SED=gsed", f"HOSTCC=cc", f"CROSS_COMPILE=${FREEBSD_XDEV_PREFIX}", configuration]
    
    try:
        subprocess.run(gmake_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError:
        print("Failed to configure U-Boot.")
        print(f"Log in {uboot_src}/_.uboot.configure.log")
        exit(1)
    
    print(configuration, file=open(os.path.join(uboot_src, "_.uboot.configured"), "w"))

def uboot_build(uboot_src):
    if os.path.isfile(os.path.join(uboot_src, "_.uboot.built")):
        print("Using U-Boot from previous build.")
        return 0

    os.chdir(uboot_src)
    print(f"Building U-Boot at {datetime.datetime.now()}")
    print(f"    (Logging to {uboot_src}/_.uboot.build.log)")
    
    # U-Boot 2014.10 chokes when csh sets VENDOR
    os.environ.pop("VENDOR", None)
    gmake_cmd = ["gmake", "SED=gsed", f"HOSTCC=cc", f"CROSS_COMPILE=${FREEBSD_XDEV_PREFIX}"]
    
    try:
        subprocess.run(gmake_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError:
        print("Failed to build U-Boot.")
        print(f"Log in {uboot_src}/_.uboot.build.log")
        exit(1)

    open(os.path.join(uboot_src, "_.uboot.built"), "w").close()

def uboot_version_from_dir(uboot_src):
    UBOOT_VERSION = re.search(r"u-boot-(\d+\.\d+)", uboot_src)
    
    if UBOOT_VERSION is None:
        UBOOT_VERSION = re.search(r"u-boot-(master)", uboot_src)
        
        if UBOOT_VERSION is None:
            UBOOT_VERSION = "unknown"
    else:
        UBOOT_VERSION = UBOOT_VERSION.group(1)
    
    return UBOOT_VERSION

def uboot_set_patch_version(uboot_src, release_version=None):
    if release_version:
        os.environ["UBOOT_PATCH_VERSION"] = release_version
    else:
        os.environ["UBOOT_PATCH_VERSION"] = uboot_version_from_dir(uboot_src)

def _uboot_check_patch_version():
    if "UBOOT_PATCH_VERSION" not in os.environ:
        print("uboot_set_patch_version needs to be called before patching, configuring, or building U-Boot")
        exit(1)

def uboot_patch_files():
    _uboot_check_patch_version()

    UBOOT_PATCH_VERSION = os.environ.get("UBOOT_PATCH_VERSION")
    if UBOOT_PATCH_VERSION != "unknown":
        return f"{BOARDDIR}/files/uboot-{UBOOT_PATCH_VERSION}_*.patch"

def uboot_port_test(port_name, binary_or_image_name):
    UBOOT_PATH = f"/usr/local/share/u-boot/{port_name}"
    
    if not os.path.exists(os.path.join(UBOOT_PATH, binary_or_image_name)):
        print(f"Please install {port_name} and re-run this script.")
        print(f"You can do this with:\n  $ sudo pkg install {port_name}")
        print("or by building the port:\n"
              f"  $ cd /usr/ports/sysutils/{port_name}\n"
              f"  $ make -DBATCH all install")
        exit(1)
    
    print(f"Found U-Boot port in:\n    {UBOOT_PATH}")

def uboot_mkimage(uboot_src, script_file, output_file):
    print("Building and Installing U-Boot script")

    MKIMAGE_INPUT = os.path.join(BOARDDIR, script_file)
    MKIMAGE_OUTPUT = output_file

    MKIMAGE = os.path.join(uboot_src, "tools/mkimage")

    try:
        subprocess.run([MKIMAGE, "-A", "arm", "-O", "FreeBSD", "-T", "script", "-C", "none", "-d", MKIMAGE_INPUT, MKIMAGE_OUTPUT],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError:
        print("Error while building and installing U-Boot script.")
        print(f"Log in {WORKDIR}/_.mkimage.log")
        exit(1)

# Assuming you have defined the necessary variables like FREEBSD_XDEV_PREFIX, UBOOT_PATCH_VERSION
# scm_update_sourcetree(FREEBSD_SRC, WORKDIR)
# source_version = scm_get_revision(FREEBSD_SRC)