# Load the user configuration file.
#
# $1 - name of the config file to load
def load_config(config_file):
    # Used in old config files, before "option ImageSize" was added.
    MB = 1000 * 1000
    GB = 1000 * MB

    if os.path.isfile(config_file):
        print(f"Loading configuration from {config_file}")
        exec(open(config_file).read())
    else:
        print(f"Could not load {config_file}")
        exit(1)

# Invoke an option, which might be in one of the board
# directories or in the top-level option directory.
def option(option_name, *args):
    OPTION = option_name
    for d in BOARDDIRS + [TOPDIR]:
        OPTIONDIR = f"{d}/option/{OPTION}"
        if os.path.exists(f"{OPTIONDIR}/setup.sh"):
            print(f"Option: {OPTION} {' '.join(args)}")
            exec(open(f"{OPTIONDIR}/setup.sh").read(), globals())
            OPTION = None
            OPTIONDIR = None
            return 0
    
    print(f"Cannot import option {OPTION}.")
    print("No setup.sh found in either:")
    for d in BOARDDIRS + [TOPDIR]:
        print(f"  * {d}/option")
    exit(1)