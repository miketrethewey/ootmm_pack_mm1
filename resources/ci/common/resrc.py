'''
Run both editing scripts
'''

import os
import subprocess

# subprocess.call(os.path.join(".", "resources", "ci", "common", "validate.py"), shell=True)
subprocess.call(os.path.join(".", "resources", "ci", "common", "resrc_new.py"), shell=True)
subprocess.call(os.path.join(".", "resources", "ci", "common", "resrc_funcs.py"), shell=True)
