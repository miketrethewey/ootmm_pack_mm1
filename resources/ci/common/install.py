'''
Reset, delete packs, copy packs, edit packs
'''
import os
import subprocess
import sys

print("> Installing...")

try:
    import pyjson5
except ImportError:
    print(" > pyjson5 not installed!")
    sys.exit(1)
try:
    from jsonschema import validate, RefResolver
except ImportError:
    print(" > jsonschema not installed!")
    sys.exit(1)

print(" > Resetting from Installer...")
subprocess.call(
    [
        "python",
        os.path.join(
            ".",
            "resources",
            "ci",
            "common",
            "reset.py"
        )
    ], shell=True)
print()

print(" > Re-sourcing from Installer...")
subprocess.call(
    [
        "python",
        os.path.join(
            ".",
            "resources",
            "ci",
            "common",
            "resrc.py"
        )
    ], shell=True)
print()
