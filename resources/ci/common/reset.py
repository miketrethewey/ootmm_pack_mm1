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
subprocess.call(["python", os.path.join(".", "resources", "ci", "common", "cleanup.py")], shell=True)

srcs = {
    "ootrando_overworldmap_hamsda": {
        "url": "https://raw.githubusercontent.com/Hamsda/EmoTrackerPacks/master/ootrando_overworldmap_hamsda.zip"
    },
    "mmrando_pink": {
        "url": ""
    }
}

print("  > Resetting included packs to installed versions...")
error = False

for src, src_data in srcs.items():
    archive_path = os.path.join("..", src + ".zip")
    if not os.path.isfile(archive_path):
        print("   > ERROR: Archive: " + archive_path + " missing!")
        if "mm" in src:
            print("   > GHA can't test MM at this time.")
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
        # sys.exit(1)
        pass
    else:
        print("   > ARCHIVE :", archive_path)
        with(zipfile.ZipFile(archive_path)) as myarchive:
            dest = os.path.join(".", src)
            print("   > DEST    :", dest)
            myarchive.extractall(dest)
            print()

    if os.path.isdir(os.path.join(".", src)):
        if "mm" in src:
            # ./[mm]/items/dungeon_items.json
            # Vanilla button "true" to true
            '''
    "loop": "true",
            '''
            print("   > BUGFIX  : ./[mm]/items/dungeon_items.json")
            with(
                open(
                    os.path.join(
                        ".",
                        src,
                        "items",
                        "dungeon_items.json"
                    ),
                    "r+",
                    encoding="utf-8"
                )
            ) as jsonFile:
                jsonLines = jsonFile.readlines()
                for i in range(2400, 2410):
                    if i < len(jsonLines) and "\"true\"" in jsonLines[i]:
                        jsonLines[i] = jsonLines[i].replace("\"true\"", "true")
                jsonFile.seek(0)
                jsonFile.truncate(0)
                jsonFile.writelines(jsonLines)

            # ./[mm]/items/options.json
            # Fix last array element that doesn't fit a dict
            '''
  },
  [




  ]
]
            '''
            print("   > BUGFIX  : ./[mm]/items/options.json")
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

            # ./[mm]/layouts/broadcast.json
            # Fix trailing comma
            '''
					  {
						"type": "item",
						"item": "bombers_code5",
						"margin": "1,4",
						"width": 12,
						"height": 16
					  },
					]
            '''
            print("   > BUGFIX  : ./[mm]/layouts/broadcast.json")
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

            # ./[mm]/locations/overworld.json
            # Remove empty element
            '''
      },
      {}
    ]
  },
            '''
            print("   > BUGFIX  : ./[mm]/locations/overworld.json")
            with(
                open(
                    os.path.join(
                        ".",
                        src,
                        "locations",
                        "overworld.json"
                    ),
                    "r+",
                    encoding="utf-8"
                )
            ) as jsonFile:
                jsonLines = jsonFile.readlines()
                jsonLines[3569 - 1] = "" + "\n"
                jsonLines[3570 - 1] = "" + "\n"
                jsonFile.seek(0)
                jsonFile.truncate(0)
                jsonFile.writelines(jsonLines)


            # ./[mm]/var_accessible/locations/overworld.json
            # Remove empty element
            '''
      },
      {}
    ]
  },
            '''
            print("   > BUGFIX  : ./[mm]/var_accessible/locations/overworld.json")
            with(
                open(
                    os.path.join(
                        ".",
                        src,
                        "var_accessible",
                        "locations",
                        "overworld.json"
                    ),
                    "r+",
                    encoding="utf-8"
                )
            ) as jsonFile:
                jsonLines = jsonFile.readlines()
                for i in range(2280, 2290):
                    if "\"$has_projectile\"" in jsonLines[i - 1]:
                        jsonLines[i - 1] = jsonLines[i - 1].replace("\"$has_projectile\"", "[\"$has_projectile\"]")
                jsonLines[2569 - 1] = "" + "\n"
                jsonLines[2570 - 1] = "" + "\n"
                for i in range(3990, 4010):
                    if "\"[$has_explosives]\"" in jsonLines[i - 1]:
                        jsonLines[i - 1] = jsonLines[i - 1].replace("\"[$has_explosives]\"", "[\"[$has_explosives]\"]")
                jsonFile.seek(0)
                jsonFile.truncate(0)
                jsonFile.writelines(jsonLines)

            # ./[mm]/var_standard/layouts/tracker.json
            # Fix int to string
            '''
            '''
            print("   > BUGFIX  : ./[mm]/var_standard/layouts/tracker.json")
            with(
                open(
                    os.path.join(
                        ".",
                        src,
                        "var_standard",
                        "layouts",
                        "tracker.json"
                    ),
                    "r+",
                    encoding="utf-8"
                )
            ) as jsonFile:
                jsonLines = jsonFile.readlines()
                for i in range(5, 15):
                    if i < len(jsonLines) and str(10) in jsonLines[i]:
                        jsonLines[i] = jsonLines[i].replace(str(10), "\"10\"")
                jsonFile.seek(0)
                jsonFile.truncate(0)
                jsonFile.writelines(jsonLines)

            # ./[mm]/var_minimal/layouts/tracker.json
            # Fix int to string
            '''
            '''
            print("   > BUGFIX  : ./[mm]/var_minimal/layouts/tracker.json")
            with(
                open(
                    os.path.join(
                        ".",
                        src,
                        "var_minimal",
                        "layouts",
                        "tracker.json"
                    ),
                    "r+",
                    encoding="utf-8"
                )
            ) as jsonFile:
                jsonLines = jsonFile.readlines()
                for i in range(270, 300):
                    if i < len(jsonLines) and str(10) in jsonLines[i - 1]:
                        jsonLines[i - 1] = jsonLines[i - 1].replace(str(10), "\"10\"")
                jsonFile.seek(0)
                jsonFile.truncate(0)
                jsonFile.writelines(jsonLines)

            print("   > COPY    : Standard tracker to global tracker")
            shutil.copy(
                os.path.join(".", src, "var_standard", "layouts", "tracker.json"),
                os.path.join(".", src, "layouts", "tracker.json")
            )
