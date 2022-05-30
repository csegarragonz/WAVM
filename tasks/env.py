from os.path import dirname, exists, realpath, join, expanduser

WAVM_ROOT = dirname(dirname(realpath(__file__)))
WAVM_SOURCE_ROOT = dirname(dirname(realpath(__file__)))
WAVM_BUILD_ROOT = "/build"
WAVM_BINARY = join(WAVM_BUILD_ROOT, "bin", "wavm")
