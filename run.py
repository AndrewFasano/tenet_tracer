import os
from shutil import copy
from sys import argv, exit, stderr
try:
    from pandare import Panda
except ImportError:
    print("Error, could not load pandare package - are you running inside the container?")

SUPPORTED_ARCHES = ["x86", "x86_64"]

def usage():
    print(f"USAGE {argv[0]} [arch] [copydir] [target] (args)")
    print(f"\tarch: " + " ".join(SUPPORTED_ARCHES))
    print(f"\tcopydir: path to directory (inside container) that will be copied into the guest")
    print(f"\ttarget: path (relative to copydir) to the binary to execute")
    print(f"\targs: optional arguments to the binary to execute")
    exit(1)

if len(argv) < 4:
    usage()

arch = argv[1]
copydir = argv[2]
target = argv[3]
args = []
if len(argv) > 4:
    args = argv[4:]

if arch not in SUPPORTED_ARCHES:
    print("Unsupported architecture")
    usage()

full_targ = f"./{copydir}/{target}" if not copydir.startswith("/") else f"{copydir}/{target}"
target_name = target.split("/")[-1]

if not os.path.isfile(full_targ):
    print(f"No such file {full_targ}")
    usage()

panda = Panda(generic=arch)

# Drive guest such that it executs our target   
@panda.queue_blocking
def driver():
    panda.revert_sync("root")
    panda.copy_to_guest(copydir, absolute_paths=True)
    panda.run_serial_cmd(f"chmod +x {full_targ}")
    panda.run_serial_cmd(f"cd {copydir}")
    panda.load_plugin("trace", {"target": target_name, 'log': "trace.log"})
    print(panda.run_serial_cmd(f"./{target} {' '.join(args)}"))

    panda.end_analysis()

# Extra information: print the base address target is loaded at to stderr
@panda.ppp("proc_start_linux", "on_rec_auxv")
def proc_start(cpu, tb, auxv):
    procname = panda.ffi.string(auxv.argv[0]).decode(errors='ignore') if auxv.argv[0] != panda.ffi.NULL else "(error)"

    if target_name in procname:
        print(f"{procname} loaded at 0x{auxv.program_header:x}")


panda.run()
copy("trace.log", full_targ+".log")
print(f"\nTrace collection finished. Log is at {full_targ}.log")
