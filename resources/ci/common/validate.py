# pylint: disable=unnecessary-pass
# pylint: disable=invalid-name
'''
Validate JSON against provided schema
'''
import os
import json
import ssl
import urllib.request
import pyjson5
from pathlib import Path
from jsonschema import validate, RefResolver

def check_files(resrcDirs):
    '''
    Check files recursively
    '''
    # cycle through dirs
    for resrcDir in resrcDirs:
        # cycle through this dir
        jsonType = ""
        for jsonTypeCheck in ["items", "layouts", "locations"]:
            if jsonTypeCheck in resrcDir:
                jsonType = jsonTypeCheck
        if "maps" in resrcDir:
            continue
        if jsonType != "":
            for r, _, f in os.walk(resrcDir):
                for filename in f:
                    # open file
                    filePath = os.path.join(r, filename)
                    print("  " + filePath)
                    with open(filePath, "r", encoding="utf-8") as jsonFile:
                        fileJSON = pyjson5.decode_io(jsonFile)
                        result = validate(
                            instance=fileJSON,
                            schema=schemas["emo"][jsonType],
                            resolver=RefResolver(
                                base_uri=schemaURI,
                                referrer=schemas["emo"][jsonType]
                            )
                        )
                        if result:
                            print("     " + "INVALID")
                            pass
        else:
            print("TYPE NOT FOUND: " + resrcDir)
            print()

schemas = {}
schemaSrcs = [
  "https://emotracker.net/developers/schemas/items.json",
  # "https://emotracker.net/developers/schemas/layouts.json",
  "https://emotracker.net/developers/schemas/locations.json"
]

schemaDir = os.path.join(".", "schema")
print("DOWNLOAD SCHEMAS")
if not os.path.isdir(schemaDir):
    os.makedirs(schemaDir)
for url in schemaSrcs:
    context = ssl._create_unverified_context()
    schema_req = urllib.request.urlopen(url, context=context)
    schema_data = schema_req.read()
    if not os.path.isfile(os.path.join(schemaDir, os.path.basename(url))):
        with open(os.path.join(schemaDir, os.path.basename(url)), "wb") as schema_file:
            schema_file.write(schema_data)

print("LOAD SCHEMAS")
schemaAbsPath = os.path.abspath(schemaDir)
schemaURI = Path(schemaAbsPath).as_uri() + "/"
for schemaFileName in os.listdir(schemaDir):
    if os.path.isfile(os.path.join(schemaDir, schemaFileName)):
        with open(
            os.path.join(
                schemaDir,
                schemaFileName
            ),
            "r",
            encoding="utf-8"
        ) as schemaFile:
            gameKey = "emo"
            schemaKey = schemaFileName.replace(".json", "")
            if gameKey not in schemas:
                schemas[gameKey] = {}
            schemas[gameKey][schemaKey] = json.load(schemaFile)

print("VALIDATE")
srcs = {
    "oot": {
        "packUID": "ootrando_overworldmap_hamsda",
        "variants": [
            "var_itemsonly",
            "var_itemsonly_keysanity",
            "var_minimalist"
        ]
    },
    "mm": {
        "packUID": "mmrando_pink",
        "variants": [
            "var_accessible",
            "var_maptracker",
            "var_minimal",
            "var_standard"
        ]
    }
}

for [gameID, packData] in srcs.items():
    packUID = packData["packUID"]
    variants = packData["variants"]
    if os.path.isdir(os.path.join(".", packUID)):
        print(gameID, packUID)
        layoutKeyMap = {}
        resrcDirs = [
            os.path.join(".", packUID, "items"),
            os.path.join(".", packUID, "layouts"),
            os.path.join(".", packUID, "locations"),
            os.path.join(".", packUID, "maps")
        ]
        # print(resrcDirs)
        check_files(resrcDirs)

        for variant in variants:
            layoutKeyMap = {}
            resrcDirs = {
                os.path.join(".", packUID, variant, "items"),
                os.path.join(".", packUID, variant, "layouts"),
                os.path.join(".", packUID, variant, "locations"),
                os.path.join(".", packUID, variant, "maps")
            }
            # print(resrcDirs)
            check_files(resrcDirs)
