'''
Run both editing scripts
'''

import os
import sys
import subprocess

print(" > Starting Re-sourcer...")

try:
    import pyjson5
except ImportError:
    print("  > pyjson5 not installed!")
    sys.exit(1)
try:
    from jsonschema import validate, RefResolver
except ImportError:
    print("  > jsonschema not installed!")
    sys.exit(1)


print("  > Validating from Re-sourcer...")
subprocess.call(
    [
        "python",
        os.path.join(
            ".",
            "resources",
            "ci",
            "common",
            "validate.py"
        )
    ], shell=True)
print()

print("  > Managing most from Re-sourcer...")
subprocess.call(
    [
        "python",
        os.path.join(
            ".",
            "resources",
            "ci",
            "common",
            "resrc_new.py"
        )
    ], shell=True)
print()

print("  > Managing functions from Re-sourcer...")
subprocess.call(
    [
        "python",
        os.path.join(
            ".",
            "resources",
            "ci",
            "common",
            "resrc_funcs.py"
        )
    ], shell=True)
print()

print("  > Re-Validating from Re-sourcer...")
subprocess.call(
    [
        "python",
        os.path.join(
            ".",
            "resources",
            "ci",
            "common",
            "validate.py"
        )
    ], shell=True)
print()
