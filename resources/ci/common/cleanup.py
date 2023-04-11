'''
Revert to base state
'''
import os
import shutil

srcs = [
    "ootrando_overworldmap_hamm1sda-new",
    "ootrando_overworldmap_hamm1sda",
    "ootrando_overworldmap_hamsda",
    "mmrando_pink"
]

print("   > Cleaning up from Cleaner...")
print("    > Deleting included packs...")

for src in srcs:
    rm = os.path.join(".", src)
    print("     > REMOVING: ", rm)
    if os.path.isdir(rm):
        print("     > REMOVED : ", rm)
        shutil.rmtree(rm)
    print()
