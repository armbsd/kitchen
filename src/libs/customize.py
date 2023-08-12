# Crochet defines a handful of standard shell functions
# to support end-user customization. These are never
# defined or overridden by board or option definitions.

# def customize_boot_partition(): pass
# def customize_freebsd_partition(): pass
# def customize_post_unmount(): pass

# If any of the above are actually defined, add them to the
# strategy. We deliberately add them with a late priority.
def install_customize_hooks():
    if 'customize_boot_partition' in globals():
        PRIORITY = 200
        strategy_add(PHASE_BOOT_INSTALL, customize_boot_partition)
    if 'customize_freebsd_partition' in globals():
        PRIORITY = 200
        strategy_add(PHASE_FREEBSD_USER_CUSTOMIZATION, customize_freebsd_partition)
    if 'customize_post_unmount' in globals():
        PRIORITY = 200
        strategy_add(PHASE_POST_UNMOUNT, customize_post_unmount)

strategy_add(PHASE_POST_CONFIG, install_customize_hooks)

# Copy overlay files early in the user customization phase.
# Typically, people want to copy static files and then
# tweak them afterwards.
def customize_overlay_files():
    real_mountpoint = os.path.realpath(BOARD_FREEBSD_MOUNTPATH)
    if os.path.isdir(f"{TOPDIR}/overlay"):
        print(f"Overlaying files from {TOPDIR}/overlay")
        subprocess.run(["cd", f"{TOPDIR}/overlay", "&&", "pax", "-rw", ".", real_mountpoint], shell=True, check=True)
    if os.path.isdir(f"{WORKDIR}/overlay"):
        print(f"Overlaying files from {WORKDIR}/overlay")
        subprocess.run(["cd", f"{WORKDIR}/overlay", "&&", "pax", "-rw", ".", real_mountpoint], shell=True, check=True)

PRIORITY = 50
strategy_add(PHASE_FREEBSD_USER_CUSTOMIZATION, customize_overlay_files)