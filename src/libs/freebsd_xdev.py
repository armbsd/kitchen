import os
import shutil
import subprocess

def freebsd_xdev_test():
    xdev_arch = os.environ['TARGET_ARCH']
    xdev_arch_map = {
        'arm*': 'arm',
        'mips*': 'mips',
        'pc98': 'i386',
        'powerpc*': 'powerpc',
    }

    xdev_arch_matched = False
    for pattern, xdev in xdev_arch_map.items():
        if fnmatch.fnmatch(xdev_arch, pattern):
            xdev_arch_matched = True
            break

    if not xdev_arch_matched:
        xdev = xdev_arch

    freebsd_xdev_prefix = f"/usr/{xdev_arch}-freebsd/usr/bin/"
    cc_path = shutil.which('cc', path=freebsd_xdev_prefix)

    if cc_path is None:
        print("Can't find appropriate FreeBSD xdev tools.")
        print(f"Tested: {cc_path}")
        print("If you have FreeBSD-CURRENT sources in /usr/src, you can build these with the following command:")
        print("")
        print(f"cd /usr/src && sudo make XDEV={xdev} XDEV_ARCH={xdev_arch} WITH_GCC=1 WITH_GCC_BOOTSTRAP=1 WITHOUT_CLANG=1 WITHOUT_CLANG_BOOTSTRAP=1 WITHOUT_CLANG_IS_CC=1 WITHOUT_TESTS=1 xdev")
        print("")
        print("Run this script again after you have the xdev tools installed.")
        exit(1)

    try:
        include_dir = subprocess.check_output([cc_path, '-print-file-name=include'], text=True).strip()
        if not os.path.exists(os.path.join(include_dir, 'stdarg.h')):
            print("FreeBSD xdev tools are broken.")
            print("The following command should print the full path to a directory")
            print("containing stdarg.h and other basic headers suitable for this target:")
            print(f"  $ {cc_path} -print-file-name=include")
            print("Please install a newer version of the xdev tools.")
            exit(1)
        print(f"Found FreeBSD xdev tools for {xdev_arch}")
    except subprocess.CalledProcessError:
        print("Error while checking xdev tools.")
        exit(1)

# Call the function
freebsd_xdev_test()