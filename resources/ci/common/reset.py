# pylint: disable=protected-access
'''
Reset, delete packs, copy packs, bugfixes
'''

import os
import shutil
import ssl
import subprocess
import sys
import urllib.request
import zipfile

print("  > Cleaning up from Resetter...")
subprocess.call(os.path.join(".", "resources", "ci", "common", "cleanup.py"), shell=True)

srcs = {
    "ootrando_overworldmap_hamsda": {
        "url": "https://raw.githubusercontent.com/Hamsda/EmoTrackerPacks/master/ootrando_overworldmap_hamsda.zip"
    },
    "mmrando_pink": {
        "url": ""
    }
}

print("Resetting included packs to installed versions...")
error = False

for src, src_data in srcs.items():
    archive_path = os.path.join("..", src + ".zip")
    if not os.path.isfile(archive_path):
        print("ERROR: Archive: " + archive_path + " missing!")
        if "mm" in src:
            print("GHA can't test MM at this time.")
        error = True
        if "ootrando" in src:
            if "url" in src_data:
                url = src_data["url"]
                context = ssl._create_unverified_context()
                archive_req = urllib.request.urlopen(url, context=context)
                archive_data = archive_req.read()
                with open(archive_path, "wb") as archive_file:
                    archive_file.write(archive_data)
                error = False
    if error:
        sys.exit(1)
    else:
        print("ARCHIVE:", archive_path)
        with(zipfile.ZipFile(archive_path)) as myarchive:
            dest = os.path.join(".", src)
            print("DEST   :", dest)
            myarchive.extractall(dest)

    if "mm" in src:
        with(
            open(
                os.path.join(
                    ".",
                    src,
                    "items",
                    "options.json"
                ),
                "r+",
                encoding="utf-8"
            )
        ) as jsonFile:
            jsonLines = jsonFile.readlines()
            for i in range(140, 147):
                jsonLines[i - 1] = ""
            jsonLines[140 - 1] = "}" + "\n"
            jsonFile.seek(0)
            jsonFile.truncate(0)
            jsonFile.writelines(jsonLines)
        with(
            open(
                os.path.join(
                    ".",
                    src,
                    "layouts",
                    "broadcast.json"
                ),
                "r+",
                encoding="utf-8"
            )
        ) as jsonFile:
            jsonLines = jsonFile.readlines()
            jsonLines[104 - 1] = "}" + "\n"
            jsonFile.seek(0)
            jsonFile.truncate(0)
            jsonFile.writelines(jsonLines)
        shutil.copy(
            os.path.join(".", src, "var_standard", "layouts", "tracker.json"),
            os.path.join(".", src, "layouts", "tracker.json")
        )
    print()
