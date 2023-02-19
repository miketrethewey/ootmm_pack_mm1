'''
Run both editing scripts
'''

import os
import subprocess

print("  > Validating from Re-sourcer...")
subprocess.call(["python", os.path.join(".", "resources", "ci", "common", "validate.py")], shell=True)
print()

print("  > Managing most from Re-sourcer...")
subprocess.call(["python", os.path.join(".", "resources", "ci", "common", "resrc_new.py")], shell=True)
print()

print("  > Managing functions from Re-sourcer...")
subprocess.call(["python", os.path.join(".", "resources", "ci", "common", "resrc_funcs.py")], shell=True)
print()
