"""
Reset, delete packs, copy packs, edit packs
"""
import os
import subprocess

subprocess.call(os.path.join(".", "resources", "ci", "common", "reset.py"), shell=True)
subprocess.call(os.path.join(".", "resources", "ci", "common", "resrc.py"), shell=True)
