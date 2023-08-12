import os
import shutil
import logging
from .executor import execute

log = logging.getLogger(__name__)



# Board setup should not touch these, so users can
FREEBSD_SRC = '/usr/src'
FREEBSD_EXTRA_ARGS = ""
FREEBSD_WORLD_EXTRA_ARGS = ""
FREEBSD_BUILDWORLD_EXTRA_ARGS = ""
FREEBSD_INSTALLWORLD_EXTRA_ARGS = ""
FREEBSD_KERNEL_EXTRA_ARGS = ""
FREEBSD_BUILDKERNEL_EXTRA_ARGS = ""
FREEBSD_INSTALLKERNEL_EXTRA_ARGS = ""

# Set other variables as needed
# ...

def freebsd_default_makeobjdirprefix():
    if 'MAKEOBJDIRPREFIX' not in os.environ:
        os.environ['MAKEOBJDIRPREFIX'] = os.path.join(os.environ['WORKDIR'], 'obj')

def freebsd_download_instructions(*commands):
    print("\nYou can obtain a suitable FreeBSD source tree with the following commands:")
    for cmd in commands:
        print(cmd)
    print("\nSet $FREEBSD_SRC in {CONFIGFILE:-the -c <config file>} if you have the sources in a different directory.")
    print("Run this script again after you have the sources installed.")
    exit(1)

def freebsd_dtc_test():
    if shutil.which('dtc') is None:
        print("You need the dtc compiler installed on your system.")
        print("Newer versions of FreeBSD have this installed by default.")
        print("On older FreeBSD versions:")
        print("  $ cd /usr/src/usr.bin/dtc")
        print("  $ make")
        print("  $ make install")
        print("")
        print("Rerun this script after you install it.")
        exit(1)

def freebsd_src_version():
    with open(os.path.join(FREEBSD_SRC, 'sys/conf/newvers.sh')) as vers_file:
        for line in vers_file:
            if line.startswith("REVISION="):
                freebsd_version = line.split('=')[1].strip().strip('"')
                freebsd_major_version = freebsd_version.split('.')[0]
                print(f"Building FreeBSD version: {freebsd_version}")
                return freebsd_version, freebsd_major_version

def freebsd_objdir():
    freebsd_major_version = freebsd_src_version()[1]

    if freebsd_major_version == '8':
        freebsd_objdir = os.path.join(os.environ['MAKEOBJDIRPREFIX'], f"{os.environ['TARGET_ARCH']}{FREEBSD_SRC}")
    elif int(freebsd_major_version) >= 9:
        buildenv = f"make -C {FREEBSD_SRC} TARGET_ARCH={os.environ['TARGET_ARCH']} buildenvvars"
        makeobjdirprefix = os.path.join(os.environ['MAKEOBJDIRPREFIX'], eval(buildenv).get('MAKEOBJDIRPREFIX', ''), os.path.realpath(FREEBSD_SRC))
        freebsd_objdir = makeobjdirprefix
    else:
        freebsd_objdir = None  # Add appropriate handling for other versions

    if freebsd_objdir:
        print("Object files are at:", freebsd_objdir)
    else:
        print("Object directory determination is not yet supported for this FreeBSD version.")

# Add more translated functions here...

# Example usage
# freebsd_default_makeobjdirprefix()
# freebsd_download_instructions(
#     "$ svn co https://svn.freebsd.org/base/head $FREEBSD_SRC"
# )
# freebsd_dtc_test()
# freebsd_src_version()
# freebsd_objdir()
# Call other functions as needed...