# TODO - must ensure CRIU is installed
from invoke import task
from os import makedirs
from os.path import join
from tasks.env import WAVM_BINARY, WAVM_SOURCE_ROOT
from subprocess import run, PIPE, STDOUT, Popen

COUNTER_PROGRAM = join(WAVM_SOURCE_ROOT, "Examples", "counter.wasm")
CRIU_BINARY = join("/tmp/criu-3.17/criu/criu")
CRIU_DUMP_DIR = "/tmp/criu"


def _get_process_pid(proc_string):
    pgrep_cmd = "pgrep -f '{}'".format(proc_string)
    print(pgrep_cmd)
    out = run(pgrep_cmd,
              shell=True, stdout=PIPE,
              stderr=STDOUT)
    return int(out.stdout.decode().strip().split("\n")[0])


@task
def checkpoint(ctx):
    """
    Checkpoint (and stop) the counter program using CRIU
    """
    pid = _get_process_pid("{} run".format(WAVM_BINARY))
    # Create random temporary dir for the images
    makedirs(CRIU_DUMP_DIR, exist_ok=True)
    criu_cmd = [
        CRIU_BINARY,
        "dump",
        "--images-dir {}".format(CRIU_DUMP_DIR),
        "--shell-job",
        "-t {}".format(pid),
    ]
    criu_cmd = " ".join(criu_cmd)
    print(criu_cmd)
    run(criu_cmd, check=True, shell=True)


@task
def restart(ctx):
    """
    Restart the checkpointed counter program using CRIU
    """
    # Create random temporary dir for the images
    makedirs(CRIU_DUMP_DIR, exist_ok=True)
    criu_cmd = [
        CRIU_BINARY,
        "restore",
        "--images-dir {}".format(CRIU_DUMP_DIR),
        "--shell-job",
    ]
    criu_cmd = " ".join(criu_cmd)
    print(criu_cmd)
    run(criu_cmd, check=True, shell=True)


@task
def start(ctx, num_loops):
    """
    Start counter function for C/R demo with CRIU
    """
    wavm_cmd = [
        WAVM_BINARY,
        "run",
        COUNTER_PROGRAM,
        num_loops,
    ]
    print(" ".join(wavm_cmd))
    Popen(wavm_cmd)
