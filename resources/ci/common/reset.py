# pylint: disable=invalid-name, line-too-long, pointless-string-statement, protected-access
'''
Reset, delete packs, copy packs, bugfixes
'''

import json
import os
import shutil
import ssl
import subprocess
import urllib.request
import zipfile
import pyjson5

print("  > Cleaning up from Resetter...")
subprocess.call(
    [
        "python",
        os.path.join(
            ".",
            "resources",
            "ci",
            "common",
            "cleanup.py"
        )
    ], shell=True)

srcs = {
    "ootrando_overworldmap_hamm1sda": {
        "url": "https://github.com/" + \
            "miketrethewey/ootrando_overworldmap_hamm1sda/" + \
            "archive/refs/heads/" + \
            "unstable.zip"
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
                with urllib.request.urlopen(url, context=context) as archive_req:
                    archive_data = archive_req.read()
                    with open(archive_path, "wb") as archive_file:
                        print("   > DOWNLOAD:", src)
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
            for item in os.listdir(dest):
                if src in item and os.path.isdir(os.path.join(dest, item)):
                    print("   > MOVE    :", os.path.join(dest, item), "->", os.path.join(".", src))
                    # copy nested folder to new "root" folder
                    # print(f"COPY  : {os.path.join(dest, item)} -> {os.path.join('.', src + '-new')}")
                    shutil.copytree(
                        os.path.join(dest, item),
                        os.path.join(".", src + "-new")
                    )
                    # delete nested folder
                    # print(f"DELETE: {os.path.join(dest, item)}")
                    shutil.rmtree(
                        os.path.join(dest, item)
                    )
                    # delete old folder
                    # print(f"DELETE: {os.path.join(dest)}")
                    shutil.rmtree(
                        os.path.join(dest)
                    )
                    # rename "new" folder
                    # print(f"MOVE  : {os.path.join('.', src + '-new')} -> {os.path.join('.', src)}")
                    shutil.move(
                        os.path.join(".", src + "-new"),
                        os.path.join(".", src)
                    )
            print()
    exit(1)

    if os.path.isdir(os.path.join(".", src)):
        if "mm" in src:
            # ./[mm]/manifest.json
            # Add platform ID
            '''
            "platform": "n64"
            '''
            print("   > BUGFIX  : ./[mm]/manifest.json")
            with(
                open(
                    os.path.join(
                        ".",
                        src,
                        "manifest.json"
                    ),
                    "r+",
                    encoding="utf-8-sig"
                )
            ) as jsonFile:
                manifestJSON = json.load(jsonFile)
                manifestJSON["platform"] = "n64"
                jsonFile.seek(0)
                jsonFile.truncate(0)
                jsonFile.write(json.dumps(manifestJSON, indent=2))

            # ./[mm]/items/dungeon_items.json
            # Vanilla button "true" to true
            '''
            "loop": "true"
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
                    encoding="utf-8-sig"
                )
            ) as jsonFile:
                jsonLines = jsonFile.readlines()
                for i in range(2400, 2410):
                    if i < len(jsonLines) and "\"true\"" in jsonLines[i]:
                        jsonLines[i] = jsonLines[i].replace("\"true\"", "true")
                jsonFile.seek(0)
                jsonFile.truncate(0)
                jsonFile.writelines(jsonLines)

            # ./[mm]/items/dungeon_items.json
            # Update logic for Combo Rando
            '''
            Disable starting MM Ocarina & MM Song of Time
            '''
            print("   > HOTFIX  : ./[mm]/items/dungeon_items.json")
            with(
                open(
                    os.path.join(
                        ".",
                        src,
                        "items",
                        "dungeon_items.json"
                    ),
                    "r+",
                    encoding="utf-8-sig"
                )
            ) as jsonFile:
                jsonData = pyjson5.decode_io(jsonFile)
                for item in jsonData:
                    if "name" in item:
                        if item["name"] in [ "Ocarina", "Song of Time" ]:
                            item["initial_active_state"] = False
                jsonFile.seek(0)
                jsonFile.truncate(0)
                jsonFile.write(json.dumps(jsonData, indent=2))

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
                        jsonLines[i - 1] = jsonLines[i - 1].replace(
                            "\"$has_projectile\"",
                            "[\"$has_projectile\"]"
                        )
                jsonLines[2569 - 1] = "" + "\n"
                jsonLines[2570 - 1] = "" + "\n"
                for i in range(3990, 4010):
                    if "\"[$has_explosives]\"" in jsonLines[i - 1]:
                        jsonLines[i - 1] = jsonLines[i - 1].replace(
                            "\"[$has_explosives]\"",
                            "[\"[$has_explosives]\"]"
                        )
                jsonFile.seek(0)
                jsonFile.truncate(0)
                jsonFile.writelines(jsonLines)

            # ./[mm]/locations/overworld.json
            # Add Rando access requirements for MM
            '''
            Majora's Mask entry logic: MM Ocarina, MM Song of Time
            '''
            print("   > HOTFIX  : ./[mm]/locations/overworld.json")
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
                jsonData = pyjson5.decode_io(jsonFile)
                jsonData.insert(
                    0,
                    {
                      "name": "Termina",
                      "access_rules": [
                        "[]",
                        "mm_ocarina,mm_time"
                      ]
                    }
                )
                jsonData[1]["parent"] = "Termina"
                jsonData[2]["parent"] = "Termina"
                jsonData[3]["parent"] = "Termina"
                jsonFile.seek(0)
                jsonFile.truncate(0)
                jsonFile.write(json.dumps(jsonData))

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
        elif "ootrando" in src:
            # ./[oot]/manifest.json
            # Add platform ID
            '''
            "platform": "n64"
            '''
            print("   > BUGFIX  : ./[oot]/manifest.json")
            with(
                open(
                    os.path.join(
                        ".",
                        src,
                        "manifest.json"
                    ),
                    "r+",
                    encoding="utf-8-sig"
                )
            ) as jsonFile:
                manifestJSON = json.load(jsonFile)
                manifestJSON["platform"] = "n64"
                jsonFile.seek(0)
                jsonFile.truncate(0)
                jsonFile.write(json.dumps(manifestJSON, indent=2))

            # ./[oot]/locations/overworld.json
            '''
            Fix Kak GS Watchtower
              Needs Chus but not just bombs
            Fix Mask Shop
              Except not because rando
            Fix HC Garden
              Song from Impa & Zelda's Letter require 'oot_childcucco_used', not 'oot_childcucco'
            Fix Malon at Castle
              Add hosted "Malon met at Castle" storymarker
            Fix Song from Malon
              Requires 'oot_ocarina' and "Malon met at Castle" collected
            '''
            print("   > BUGFIX  : ./[oot]/locations/overworld.json")
            with(
                open(
                    os.path.join(
                        ".",
                        src,
                        "locations",
                        "overworld.json"
                    ),
                    "r+",
                    encoding="utf-8-sig"
                )
            ) as jsonFile:
                locationsJSON = json.load(jsonFile)
                # Fix Kak GS Watchtower (N)
                # location = locationsJSON[0]["children"][2]["children"][1]["children"][15]["sections"][4]
                # print(location)
                # location["access_rules"][1] = location["access_rules"][1].replace("$has_bombchus", "$has|oot_bombchu")
                # locationsJSON[0]["children"][2]["children"][1]["children"][15]["sections"][4] = location

                # Fix Mask Shop
                #  except don't for OoT/MM Rando
                #  Hyrule Town/Market/Market Mask Shop
                location = locationsJSON[0]["children"][2]["children"][3]["children"][0]["children"][2]
                # print(location["name"])
                if location["name"] == "Market Mask Shop":
                    for i, section in enumerate(location["sections"]):
                        section["item_count"] = 1
                        location["sections"][i] = section
                    # locationsJSON[0]["children"][2]["children"][3]["children"][0]["children"][2] = location
                    # print(f"    > Fixed {location['name']}")

                # Fix HC Garden
                #  Hyrule Castle Grounds/HC Garden
                location = locationsJSON[0]["children"][2]["children"][3]["children"][1]["children"][2]
                # print(location["name"])
                if location["name"] == "HC Garden":
                    location["access_rules"][0] = location["access_rules"][0].replace("cucco","cucco_used")
                    locationsJSON[0]["children"][2]["children"][3]["children"][1]["children"][2] = location
                    print(f"    > Fixed {location['name']}")

                # Fix Impa's House HP
                #  Kakariko Village/Kak Impas House Back/Kak Impas House Freestanding PoH
                location = locationsJSON[0]["children"][2]["children"][1]["children"][2]["sections"][0]
                # print(location["name"])
                if location["name"] == "Kak Impas House Freestanding PoH":
                    location["access_rules"] = [
                        "$oot_has_age|child,oot_bombs",
                        "$oot_has_age|adult,oot_hookshot"
                    ]
                    locationsJSON[0]["children"][2]["children"][1]["children"][2]["sections"][0] = location
                    print(f"    > Fixed {location['name']}")

                # Fix Malon at Castle
                #  Hyrule Castle Grounds/Malon at Castle
                location = locationsJSON[0]["children"][2]["children"][3]["children"][1]["children"][0]["sections"][0]
                # print(location["name"])
                if location["name"] == "HC Malon Egg":
                    location["hosted_item"] = "oot_malon_met_castle"
                    locationsJSON[0]["children"][2]["children"][3]["children"][1]["children"][0]["sections"][0] = location
                    print(f"    > Fixed {location['name']}")

                # Fix Song from Malon
                #  Lon Lon Ranch/Malon at Ranch/Song from Malon
                location = locationsJSON[0]["children"][2]["children"][0]["children"][11]["children"][0]["sections"][0]
                # print(location["name"])
                if location["name"] == "Song from Malon":
                    location["access_rules"] = [
                      "$oot_has_age|child,oot_ocarina,oot_malon_met_castle"
                    ]
                    location["hosted_item"] = "oot_malon_met_castle"
                    locationsJSON[0]["children"][2]["children"][0]["children"][11]["children"][0]["sections"][0] = location
                    print(f"    > Fixed {location['name']}")

                jsonFile.seek(0)
                jsonFile.truncate(0)
                jsonFile.write(json.dumps(locationsJSON, indent=2))

            # ./[oot]/scripts/cached_helpers.json
            # Always invalidate cache
            '''
            '''
            print("   > BUGFIX  : ./[oot]/scripts/cached_helpers.json")
            with(
                open(
                    os.path.join(
                        ".",
                        src,
                        "scripts",
                        "cached_helpers.lua"
                    ),
                    "r+",
                    encoding="utf-8"
                )
            ) as luaFile:
                luaLines = luaFile.readlines()
                inSpecial = False
                for [i, luaLine] in enumerate(luaLines):
                    if "not amount_cache[item]" in luaLine:
                        inSpecial = True
                        luaLine = "-- " + luaLine
                        luaLines[i] = luaLine
                    if "end" in luaLine and inSpecial:
                        inSpecial = False
                        luaLine = "-- " + luaLine
                        luaLines[i] = luaLine
                luaFile.seek(0)
                luaFile.truncate(0)
                luaFile.writelines(luaLines)

    print()
