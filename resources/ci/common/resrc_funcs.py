# pylint: disable=invalid-name
'''
Rename and fix sources within functions
'''

import os
import re

packUID = ""
gameID = ""

funcMap = {}

print("  > Starting Function Re-sourcer...")
print("   > Re-sourcing Functions from Function Re-sourcer...")

def check_for_codes(luaLine):
    '''
    Check for codes section
    '''
    return "local codes" in luaLine.strip()


def check_for_items(luaLine):
    '''
    Check for items section
    '''
    return "--items" in luaLine.strip()


def check_for_rewards(luaLine):
    '''
    Check for rewards section
    '''
    return "local rewards" in luaLine.strip()


def check_calls(luaLine):
    '''
    Update function calls
    '''
    for [funcName, funcNew] in funcMap.items():
        if funcName + "(" in luaLine.strip() and \
                (funcNew + "(" not in luaLine.strip()):
            luaLine = luaLine.replace(
                funcName + "(",
                funcNew + "("
            )

    # update has() helper calls
    pattern = r"(?:" + gameID + \
        r"\_)(?:has)(?:[\w]*)(?:[\(])(?:[\"])([\$]?)([\w\|]*)(?:[\"])"
    matches = re.findall(pattern, luaLine)
    if matches:
        for match in matches:
            srch = match
            repl = gameID + "_"
            check = srch
            if isinstance(srch, tuple):
                check = srch[1]
            if check not in ["adult", "child", "both"]:
                if repl not in check:
                    if isinstance(srch, tuple):
                        repl = srch[0] + repl + srch[1]
                    luaLine = luaLine.replace(
                        '"' + "".join(srch) + '"',
                        '"' + repl + '"'
                    )

    # update get_object() helper calls
    pattern = r"(?:" + gameID + \
        r"\_)(?:get_object)(?:[\w]*)(?:[\(])(?:[\"])([\w]*)(?:[\"])"
    matches = re.findall(pattern, luaLine)
    if matches:
        for match in matches:
            srch = match
            repl = gameID + "_"
            if repl not in srch:
                luaLine = luaLine.replace(
                    '"' + srch + '"',
                    '"' + repl + srch + '"'
                )

    # update cache() helper calls
    pattern = r"(?:" + gameID + \
        r"\_)(?:not_like_cache)(?:[\w]*)(?:[\(])(?:[\"])([\w]*)(?:[\"])"
    matches = re.findall(pattern, luaLine)
    if matches:
        for match in matches:
            srch = match
            repl = gameID + "_"
            if repl not in srch:
                luaLine = luaLine.replace(
                    '"' + srch + '"',
                    '"' + repl + srch + '"'
                )

    # update Tracker calls
    pattern = r"(?:Tracker\:)(?:[\w]*)(?:ForCode)(?:[\(])(?:[\"])([\w]*)(?:[\"])(?:[\)])"
    match = re.search(pattern, luaLine)
    if match:
        srch = match.group(1)
        repl = gameID + "_"
        if repl not in srch:
            luaLine = luaLine.replace(
                '"' + srch + '"',
                '"' + repl + srch + '"'
            )

    return luaLine


def check_functions(luaLine):
    '''
    Update non-class functions
    '''
    match = re.match(r"function ([\w\_]*)(?:[\(])", luaLine)
    if match:
        srch = match.group(1)
        repl = gameID + "_"
        if srch not in funcMap:
            funcMap[srch.replace(repl, "")] = repl + srch.replace(repl, "")
        if repl not in luaLine:
            luaLine = luaLine.replace(srch, repl + srch)

    if not match:
        # class member functions
        match = re.match(r"function (\w*):(?:[\w\_]*)(?:[\(])", luaLine)
        if not match:
            # class instantiation
            match = re.match(r"(\w*) = (\w*)(?:\:extend\(\))", luaLine)
        if match:
            srch = match.group(1)
            repl = gameID.upper().replace("OOT", "OoT") + "_"
            if srch not in funcMap:
                funcMap[srch.replace(repl, "")] = repl + srch.replace(repl, "")
            if repl not in luaLine:
                if len(match.groups()) < 2:
                    luaLine = luaLine.replace(srch, repl + srch)
                elif len(match.groups()) >= 2:
                    luaLine = luaLine.replace(srch, repl + srch)
                    srch = match.group(2)
                    if "CustomItem" not in srch:
                        luaLine = luaLine.replace(srch, repl + srch)
    return luaLine


def check_images(luaLine):
    '''
    Update image filepaths
    '''
    match = re.search(r"(?:[\"])(images\/[\w\/\.]*)(?:[\"])", luaLine.strip())
    if match:
        srch = match.group(1)
        repl = packUID + "/"
        if repl not in luaLine:
            luaLine = luaLine.replace(
                '"' + srch + '"',
                '"' + repl + srch + '"'
            )
    return luaLine


def check_imports(luaLine):
    '''
    Update import references
    '''
    # Tracker:Add
    match = re.match(
        r"(?:Tracker\:Add)(?:[\w]*)(?:[\(])(?:[\"])([\w\/\.]*)(?:[\"])(?:[\)])",
        luaLine.strip()
    )
    if not match:
        match = re.match(
            r"(?:ScriptHost\:LoadScript)(?:[\w]*)(?:[\(])(?:[\"])([\w\/\.]*)(?:[\"])(?:[\)])",
            luaLine.strip()
        )
    if match:
        srch = match.group(1)
        repl = packUID + "/"
        if repl not in luaLine:
            luaLine = luaLine.replace(
                '"' + srch + '"',
                '"' + repl + srch + '"'
            )
    return luaLine


def check_settings(luaLine):
    '''
    Update settings codes
    '''
    match = re.search(r"\"(setting|tracker|logic)\_(\w*)\"", luaLine.strip())
    if match:
        srch = match.group(1) + "_" + match.group(2)
        repl = gameID + "_"
        if repl not in luaLine:
            luaLine = luaLine.replace(
                '"' + srch + '"',
                '"' + repl + srch + '"'
            )
    return luaLine


def check_files(resrcDirs, loop):
    '''
    Iterate through files
    '''
    if not loop:
        loop = 1
    for resrcDir in resrcDirs:
        for r, _, f in os.walk(resrcDir):
            for filename in f:
                if "sdk" in r:
                    pass
                else:
                    print("    " + r, filename)
                    with(open(os.path.join(r, filename), "r+", encoding="utf-8")) as luaFile:
                        luaLines = luaFile.readlines()
                        hasCodes = False
                        inSpecial = False
                        hasItems = False
                        hasRewards = False
                        for i, luaLine in enumerate(luaLines):
                            if loop == 1:
                                hasCodes = check_for_codes(luaLine)
                                hasItems = check_for_items(luaLine)
                                hasRewards = check_for_rewards(luaLine)
                                if hasCodes:
                                    inSpecial = True
                                if hasItems:
                                    inSpecial = True
                                if hasRewards:
                                    inSpecial = True
                                if inSpecial:
                                    pattern = r"(?:[\"])([\w]+)(?:[\"])(?:[,]?)"
                                    match = re.search(pattern, luaLine.strip())
                                    if match:
                                        if (gameID + "_") not in luaLine:
                                            luaLine = luaLine.replace(match.group(
                                                1), gameID + "_" + match.group(1))
                                    if "}" in luaLine.strip():
                                        inSpecial = False
                                luaLine = check_functions(luaLine)
                                luaLine = check_images(luaLine)
                                luaLine = check_imports(luaLine)
                                luaLine = check_settings(luaLine)
                            elif loop == 2:
                                luaLine = check_calls(luaLine)
                            luaLines[i] = luaLine

                        # truncate and write file
                        luaFile.seek(0)
                        luaFile.truncate(0)
                        luaFile.writelines(luaLines)


srcs = {
    "oot": {
        "packUID": "ootrando_overworldmap_hamsda",
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
        funcMap = {}
        resrcDirs = [
            os.path.join(".", packUID, "scripts")
        ]
        for variant in variants:
            varRoot = packRoot
            if "var_" in variant:
                varRoot = os.path.join(varRoot, variant)
            else:
                varRoot = os.path.join(varRoot, "variants", variant)
            if os.path.isdir(varRoot):
                funcMap = {}
                resrcDirs.append(os.path.join(".", packUID, variant, "scripts"))
        # print(resrcDirs)

        check_files(resrcDirs, 1)
        check_files(resrcDirs, 2)
        # print(funcMap)
        print()
