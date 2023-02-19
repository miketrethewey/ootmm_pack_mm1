'''
Reset, delete packs, copy packs, edit packs
'''
import os
import subprocess

print("> Installing...")
print(" > Resetting from Installer...")
subprocess.call(os.path.join(".", "resources", "ci", "common", "reset.py"), shell=True)
print()

print(" > Re-sourcing from Installer...")
subprocess.call(os.path.join(".", "resources", "ci", "common", "resrc.py"), shell=True)
print()
