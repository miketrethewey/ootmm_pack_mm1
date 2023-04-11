# pylint: disable=invalid-name
'''
Rename references in packs
'''

import json
import os
import re
import sys

print("  > Starting Main Re-sourcer...")

try:
    import pyjson5
except ImportError:
    print("   > pyjson5 not installed!")
    sys.exit(1)

packUID = ""
gameID = ""

print("   > Re-sourcing Main from Main Re-sourcer...")

def recursive_iter(obj, keys=()):
    '''
    Recurse through object while collecting keys
    '''
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from recursive_iter(v, keys + (k,))
    elif any(isinstance(obj, t) for t in (list, tuple)):
        for idx, item in enumerate(obj):
            yield from recursive_iter(item, keys + (idx,))
    else:
        yield keys, obj


def update_item(item_string):
    '''
    Add gameID to item reference
    '''
    items = item_string
    if isinstance(item_string, str):
        items = item_string.split(",")
    for i, item in enumerate(items):
        item = item.strip()
        match = re.match(
            r"^" +
            r"(?:[\"]?)" +
            r"(?P<pre>[\[\{\$]{0,2})" +
            r"(?P<Name>[\w\s]*)" +
            r"(?P<func_split>[\|\:]?)" +
            r"(?P<func_arg>[\w\s]*|[\d]{0,3})" +
            r"(?P<func_split2>[\|\:]?)" +
            r"(?P<func_arg2>[\w\s]*|[\d]{0,3})" +
            r"(?P<post>[\]\}]?)" +
            r"(?:[\"\,]{0,2})$",
            item
        )
        # 0: All
        # 1: pre-symbol
        # 2: Item Name
        # 3: func split
        # 4: func arg
        # 5: func split2
        # 6: func arg2
        # 7: post-symbol
        if match:
            if not match["Name"].startswith(gameID + "_") and match["Name"].strip() != "":
                item = match["pre"] + \
                    gameID + "_" + match["Name"].strip() + \
                    match["func_split"] + match["func_arg"].strip() + \
                    match["func_split2"] + match["func_arg2"].strip() + \
                    match["post"]
                # print(item)
        items[i] = item
    item_string = ",".join(items)
    return item_string


def check_items(data):
    '''
    Manage item references
    '''
    keys = data["keys"]
    item = data["item"]

    # flag for updating model
    modded = data["modded"]

    # if it's got an image
    if "img" in keys and not item.startswith(packUID + "/"):
        item = (packUID + "/" + item)
        modded = True
    elif "img_mods" in keys and "images/" in item and packUID not in item:
        # if it's got image mods
        item = item.replace("images/", packUID + "/images/")
        modded = True
    for codes_key in ["codes", "item_left", "item_right", "base_item"]:
        if codes_key in keys:
            codes = item.split(",")
            for i, code in enumerate(codes):
                code = codes[i].strip()
                if not code.startswith(gameID + "_"):
                    code = gameID + "_" + code
                    codes[i] = code
                    modded = True
            item = ",".join(codes)

    if modded:
        # print("CHECK ITEM:", keys, item)
        pass

    return {
        "keys": keys,
        "item": item,
        "modded": modded
    }


def check_layouts(data):
    '''
    Manage layouts references
    '''
    keys = data["keys"]
    item = data["item"]
    resrcDir = data["resrcDir"]
    foundTabbedContent = data["foundTabbedContent"]
    foundLayout = data["foundLayout"]

    # flag for updating model
    modded = data["modded"]

    # layout:tab icons
    if item == "tabbed":
        # might be tabbed content
        foundTabbedContent = True
    if "tabs" not in keys and \
        "type" in keys and \
            item != "tabbed":
        # false positive
        foundTabbedContent = False
    # actual positive
    if foundTabbedContent and "icon" in keys and packUID not in item:
        item = (packUID + "/" + item)
        modded = True

    # layout:layout defns & refs
    if ("layouts" in resrcDir) or ("type" in keys and item == "layout"):
        foundLayout = True
        itemCheck = update_item(keys[0])
        if itemCheck != item:
            layoutKeyMap[keys[0]] = itemCheck

    # layout:layout refs
    if foundLayout and ("layout" in keys or "key" in keys):
        itemCheck = update_item(item)
        if itemCheck != "item":
            item = itemCheck
            modded = True
        # reset helper
        foundLayout = False

    # layout:item refs
    if "rows" in keys:
        if item != "":
            itemCheck = update_item(item)
            item = itemCheck
            modded = True

    # layout:settings refs
    if ("access_rules" in keys) or \
        ("hosted_item" in keys) or \
        ("visibility_rules" in keys) or \
        ("force_invisibility_rules" in keys) or \
            ("item" in keys):
        itemCheck = update_item(item)
        if itemCheck != item:
            item = itemCheck
            modded = True

    if modded:
        # print("CHECK LAYOUT:", keys, item)
        pass

    return {
        "keys": keys,
        "item": item,
        "modded": modded,
        "foundLayout": foundLayout,
        "foundTabbedContent": foundTabbedContent
    }


def check_locations(data):
    '''
    Manage locations references
    '''
    keys = data["keys"]
    item = data["item"]

    # flag for updating model
    modded = data["modded"]

    # location:location images
    for key in [
        "chest_unopened_img",
        "chest_opened_img"
    ]:
        if key in keys and packUID not in item:
            item = (packUID + "/" + item)
            modded = True

    # location:location capture layout
    if "capture_item_layout" in keys and (packUID + "_") not in item:
        item = (gameID + "_" + item)
        modded = True

    if modded:
        # print("CHECK LOCATION:", item)
        pass

    return {
        "keys": keys,
        "item": item,
        "modded": modded
    }


def check_files(resrcDirs):
    '''
    Check files recursively
    '''
    # cycle through dirs
    for resrcDir in resrcDirs:
        # cycle through this dir
        for r, _, f in os.walk(resrcDir):
            for filename in f:
                # open file
                with(open(os.path.join(r, filename), "r+", encoding="utf-8")) as defnFile:
                    # print filename
                    print("    " + r, filename)
                    # parse JSON
                    defnJSON = pyjson5.decode_io(defnFile)

                    # flags
                    foundLayout = False
                    foundTabbedContent = False
                    modded = False

                    # cycle through elements
                    for keys, item in recursive_iter(defnJSON):
                        if not modded:
                            # process items
                            data = check_items({
                                "item": item,
                                "keys": keys,
                                "modded": modded
                            })
                            item = data["item"]
                            keys = data["keys"]
                            modded = data["modded"]

                        if not modded:
                            # process layouts
                            data = check_layouts({
                                "foundLayout": foundLayout,
                                "foundTabbedContent": foundTabbedContent,
                                "item": item,
                                "keys": keys,
                                "modded": modded,
                                "resrcDir": resrcDir
                            })
                            item = data["item"]
                            keys = data["keys"]
                            modded = data["modded"]
                            foundLayout = data["foundLayout"]
                            foundTabbedContent = data["foundTabbedContent"]

                        if not modded:
                            # process locations
                            data = check_locations({
                                "item": item,
                                "keys": keys,
                                "modded": modded
                            })
                            item = data["item"]
                            keys = data["keys"]
                            modded = data["modded"]

                        # if we're gonna mod it
                        #  do the mod
                        if modded:
                            evalStatement = ""
                            for key in keys:
                                evalStatement += "["
                                if isinstance(key, str):
                                    evalStatement += '"' + key + '"'
                                else:
                                    evalStatement += str(key)
                                evalStatement += "]"
                            evalStatement = "defnJSON" + evalStatement + " = "
                            if isinstance(item, str):
                                evalStatement += '"' + \
                                    item.replace('"', '\\"') + '"'
                            elif isinstance(item, int):
                                evalStatement += str(item)
                            # print(evalStatement)
                            exec(evalStatement)
                            foundLayout = False
                            foundTabbedContent = False
                            modded = False
                        else:
                            # print("DIDNT MOD:" + filename + ":" + defn["name"])
                            pass

                        # print debug info
                        if not modded and \
                            isinstance(item, str) and \
                            "images" in item and \
                                packUID not in item:
                            # print(keys, item)
                            pass

                    # make new layout defns
                    for [oldKey, newKey] in layoutKeyMap.items():
                        if oldKey in defnJSON:
                            defnJSON[newKey] = defnJSON[oldKey]
                            del defnJSON[oldKey]

                    # truncate and write file
                    defnFile.seek(0)
                    defnFile.truncate(0)
                    json.dump(defnJSON, defnFile, indent=2)


srcs = {
    "oot": {
        "packUID": "ootrando_overworldmap_hamm1sda",
        "variants": []
    },
    "mm": {
        "packUID": "mmrando_pink",
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
    elif os.path.isdir(os.path.join(".", packUID)):
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
            os.path.join(".", packUID, "items"),
            os.path.join(".", packUID, "layouts"),
            os.path.join(".", packUID, "locations"),
            os.path.join(".", packUID, "maps")
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
                    os.path.join(".", packUID, variant, "items"),
                    os.path.join(".", packUID, variant, "layouts"),
                    os.path.join(".", packUID, variant, "locations"),
                    os.path.join(".", packUID, variant, "maps")
                }
                # print(resrcDirs)
                check_files(resrcDirs)
        print()
