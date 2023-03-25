local variant = Tracker.ActiveVariantUID
if variant == "" then
  variant = "items_only"
end

-- OoT Init
print("Load OoT Init")
ScriptHost:LoadScript("ootrando_overworldmap_hamsda/scripts/init.lua")

-- MM Init
print("Load MM Init")
ScriptHost:LoadScript("mmrando_pink/scripts/init.lua")

-- Items
print("Loading Items")
Tracker:AddItems("ootmm/items/items.json")

-- Grids
print("Loading Grids")
Tracker:AddLayouts("ootmm/variants/" .. variant .. "/layouts/grids/oot.json")
Tracker:AddLayouts("ootmm/variants/" .. variant .. "/layouts/grids/mm.json")

dir = "ootmm/layouts/grids"
grids = {
  -- "oot",
  -- "mm",
  "z64",
  "grids"
}
for _, gridCat in ipairs(grids) do
  Tracker:AddLayouts(dir .. "/" .. gridCat .. ".json")
end
print("")

if string.find(variant, "map") then
  print("Map Variant; load map stuff")
else
  print("Not a Map Variant; load default stuff")
  -- Layout Defaults
  Tracker:AddLayouts("ootmm/layouts/broadcast.json")
  Tracker:AddLayouts("ootmm/layouts/tracker.json")
  print("")

  -- Legacy
  print("Satisfy Legacy Loads")
  Tracker:AddMaps("ootmm/maps/maps.json")
  Tracker:AddLocations("ootmm/locations/world.json")
  print("")
end

-- Variant Overrides
if variant ~= "items_only" then
  print("Loading Variant")
  -- Layout Overrides
  Tracker:AddLayouts("ootmm/variants/" .. variant .. "/layouts/tracker.json")               -- Main Tracker
  Tracker:AddLayouts("ootmm/variants/" .. variant .. "/layouts/tracker_capture_item.json")  -- Capture Tracker
  Tracker:AddLayouts("ootmm/variants/" .. variant .. "/layouts/tracker_horizontal.json")    -- Horizontal Tracker
  Tracker:AddLayouts("ootmm/variants/" .. variant .. "/layouts/tracker_vertical.json")      -- Vertical Tracker
  Tracker:AddLayouts("ootmm/variants/" .. variant .. "/layouts/broadcast.json")             -- Broadcast View
  print("")
end
