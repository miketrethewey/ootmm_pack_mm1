# pylint: disable=unnecessary-pass
# pylint: disable=invalid-name
'''
Validate JSON against provided schema
'''
import os
import json
import ssl
import sys
import urllib.request

print("  > Starting Validator...")

try:
    import pyjson5
except ImportError:
    print("   > pyjson5 not installed!")
    sys.exit(1)

from pathlib import Path

try:
    from jsonschema import validate, RefResolver
except ImportError:
    print("   > jsonschema not installed!")
    sys.exit(1)

def validate_file(r, filename, jsonType):
    '''
    Validate a file
    '''
    if ".json" in filename:
        # open file
        filePath = os.path.join(r, filename)
        print("    " + filePath)
        with open(filePath, "r", encoding="utf-8") as jsonFile:
            fileJSON = pyjson5.decode_io(jsonFile)
            validate(
                instance=fileJSON,
                schema=schemas["emo"][jsonType],
                resolver=RefResolver(
                    base_uri=schemaURI,
                    referrer=schemas["emo"][jsonType]
                )
            )

def check_files(resrcDirs):
    '''
    Check files recursively
    '''
    # cycle through dirs
    for resrcDir in resrcDirs:
        # cycle through this dir
        jsonType = ""
        for jsonTypeCheck in ["items", "layouts", "locations", "manifest.json", "repository.json"]:
            if jsonTypeCheck in resrcDir:
                jsonType = jsonTypeCheck.replace(".json", "")
        if "maps" in resrcDir:
            continue
        if jsonType != "":
            if os.path.isdir(resrcDir):
                for r, _, f in os.walk(resrcDir):
                    for filename in f:
                        validate_file(r, filename, jsonType)
            elif os.path.isfile(resrcDir):
                (r, f) = ("", [ resrcDir ])
                for filename in f:
                    validate_file(r, filename, jsonType)
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
print("   > DOWNLOAD SCHEMAS")
if not os.path.isdir(schemaDir):
    os.makedirs(schemaDir)
for url in schemaSrcs:
    context = ssl._create_unverified_context()
    schema_req = urllib.request.urlopen(url, context=context)
    schema_data = schema_req.read()
    if not os.path.isfile(os.path.join(schemaDir, os.path.basename(url))):
        with open(os.path.join(schemaDir, os.path.basename(url)), "wb") as schema_file:
            schema_file.write(schema_data)

print("   > LOAD SCHEMAS")
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

print("   > VALIDATE")
srcs = {
    "oot": {
        "packUID": "ootrando_overworldmap_hamsda",
        "variants": []
    },
    "mm": {
        "packUID": "mmrando_pink",
        "variants": []
    },
    "ootmm": {
        "packUID": "ootmm",
        "variants": []
    },
    "": {
        "packUID": "",
        "variants": []
    }
}

for [gameID, packData] in srcs.items():
    packUID = packData["packUID"]
    if os.path.isdir(os.path.join(".", packUID, "variants")):
        srcs[gameID]["variants"] = os.listdir(os.path.join(".", packUID, "variants"))
    else:
        for folder in os.listdir(os.path.join(".", packUID)):
            if "var_" in folder:
                thisDir = folder
                srcs[gameID]["variants"].append(thisDir)

for [gameID, packData] in srcs.items():
    packUID = packData["packUID"]
    variants = packData["variants"]
    packRoot = os.path.join(".", packUID)
    if os.path.isdir(packRoot):
        print("    " + (gameID if gameID != "" else "root"), packUID)
        layoutKeyMap = {}
        resrcDirs = [
            os.path.join(packRoot, "manifest.json"),
            os.path.join(packRoot, "repository.json"),
            os.path.join(packRoot, "items"),
            os.path.join(packRoot, "layouts"),
            os.path.join(packRoot, "locations"),
            os.path.join(packRoot, "maps")
        ]
        # print(resrcDirs)
        check_files(resrcDirs)

        for variant in variants:
            varRoot = packRoot
            if "var_" in variant:
                varRoot = os.path.join(varRoot, variant)
            else:
                varRoot = os.path.join(varRoot, "variants", variant)
            if os.path.isdir(varRoot):
                layoutKeyMap = {}
                resrcDirs = {
                    os.path.join(varRoot, "manifest.json"),
                    os.path.join(varRoot, "repository.json"),
                    os.path.join(varRoot, "items"),
                    os.path.join(varRoot, "layouts"),
                    os.path.join(varRoot, "locations"),
                    os.path.join(varRoot, "maps")
                }
                # print(resrcDirs)
                check_files(resrcDirs)
        print()
