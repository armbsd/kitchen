import os
import shutil
import subprocess

def set_phase(phase_variable, phase_value):
    globals()[phase_variable] = phase_value
    globals()["PHASE_DESCRIPTION_" + str(phase_value)] = phase_variable

def print_phase_description(phase_value):
    this_phase_description = globals().get("PHASE_DESCRIPTION_" + str(phase_value))
    if this_phase_description:
        print(this_phase_description)

# Clean out old strategies.
STRATEGYBASE = "/tmp/crochet/strategy"
if os.path.exists(STRATEGYBASE):
    strategy_files = os.listdir(STRATEGYBASE)
    for strategy_file in strategy_files:
        file_path = os.path.join(STRATEGYBASE, strategy_file)
        if os.path.isfile(file_path) and os.path.getctime(file_path) < (time.time() - (3 * 24 * 60 * 60)):
            os.remove(file_path)

os.makedirs(STRATEGYBASE, exist_ok=True)
_DATE = time.strftime("%Y.%m.%d.%H.%M.%S")
STRATEGYDIR = tempfile.mkdtemp(dir=os.path.join(STRATEGYBASE, _DATE + "-"))

PRIORITY = 100
_STRATEGY_ADD_COUNTER = 0
_CURRENT_PHASE = 0

def strategy_add(phase, *args):
    global _STRATEGY_ADD_COUNTER, _CURRENT_PHASE

    PHASE = phase
    if not PHASE.isdigit():
        print("Error: Phase not specified: strategy_add", *args)
        exit(1)
    PHASE = int(PHASE)

    if PHASE <= _CURRENT_PHASE:
        print("Error: Inserting a strategy item for a phase that has already run")
        print("    strategy_add", *args)
        exit(1)

    _STRATEGY_ADD_COUNTER += 1
    _P = "{:03d}{:03d}".format(PRIORITY, _STRATEGY_ADD_COUNTER)
    _PHASE_FILE = os.path.join(STRATEGYDIR, f"{PHASE}.sh")

    if PHASE % 10 == 1:
        os.remove(_PHASE_FILE)

    with open(_PHASE_FILE, "a") as f:
        f.write(f"__run {_P} OPTION=$OPTION OPTIONDIR=$OPTIONDIR BOARDDIR=$BOARDDIR {' '.join(args)}\n")

    with open(os.path.join(STRATEGYDIR, "phases.txt"), "a") as phases_file:
        phases_file.write(str(PHASE) + "\n")

def run_phase(P):
    _PHASE_FILE = os.path.join(STRATEGYDIR, f"{P}.sh")
    sorted_phase_file = _PHASE_FILE + ".sorted"
    
    with open(_PHASE_FILE, "r") as f:
        lines = f.readlines()
    
    # Sort by priority, then by insertion order.
    sorted_lines = sorted(lines, key=lambda line: (line.split()[0], line))
    
    with open(sorted_phase_file, "w") as f:
        f.writelines(sorted_lines)
    
    if VERBOSE > 0:
        print(f"====================> Phase {P} {print_phase_description(P)} <====================")
    
    for line in sorted_lines:
        eval(line.strip())

def run_strategy():
    while True:
        _LAST_PHASE = _CURRENT_PHASE
        with open(os.path.join(STRATEGYDIR, "phases.txt"), "r") as phases_file:
            phases = list(set(phases_file.read().splitlines()))
        
        phases.sort(key=int)
        
        for P in phases:
            P = int(P)
            if P > _CURRENT_PHASE:
                _CURRENT_PHASE = P
                run_phase(P)
                break
        
        if _LAST_PHASE == _CURRENT_PHASE:
            break

def __run(*args):
    global BOARD_CURRENT_MOUNTPOINT
    
    if _CURRENT_PHASE >= PHASE_FREEBSD_START and _CURRENT_PHASE <= PHASE_FREEBSD_DONE:
        BOARD_FREEBSD_MOUNTPOINT = board_ufs_mountpoint(1)
        BOARD_CURRENT_MOUNTPOINT = BOARD_FREEBSD_MOUNTPOINT
        os.chdir(BOARD_CURRENT_MOUNTPOINT)
    elif _CURRENT_PHASE >= PHASE_BOOT_START and _CURRENT_PHASE <= PHASE_BOOT_DONE:
        BOARD_BOOT_MOUNTPOINT = board_fat_mountpoint(1)
        BOARD_CURRENT_MOUNTPOINT = BOARD_BOOT_MOUNTPOINT
        os.chdir(BOARD_CURRENT_MOUNTPOINT)
    else:
        os.chdir(TOPDIR)
    
    if VERBOSE > 0:
        print("Running:", *args)
    
    eval(" ".join(args))

# Assuming you have defined the necessary variables like FREEBSD_SRC, WORKDIR
# scm_update_sourcetree(FREEBSD_SRC, WORKDIR)
# source_version = scm_get_revision(FREEBSD_SRC)