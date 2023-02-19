'''
Revert to base state
'''
import os
import shutil

srcs = [
    "ootrando_overworldmap_hamsda",
    "mmrando_pink"
]

print("Deleting included packs...")

for src in srcs:
    rm = os.path.join(".", src)
    print("REMOVE :", rm)
    if os.path.isdir(rm):
        shutil.rmtree(rm)
    print()
