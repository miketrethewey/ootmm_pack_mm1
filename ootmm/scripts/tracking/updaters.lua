function tracker_on_begin_loading_save_file()
  print("Loading Save File...")
  mm_tracker_on_begin_loading_save_file()
  oot_tracker_on_begin_loading_save_file()
end

function tracker_on_finish_loading_save_file()
  print("Loaded  Save File.")
  -- mm_tracker_on_finish_loading_save_file()
  oot_tracker_on_finish_loading_save_file()
end

function tracker_on_accessibility_updating()
  print("Updating Accessibility...")
  -- mm_tracker_on_accessibility_updating()
  oot_tracker_on_accessibility_updating()
end

function tracker_on_accessibility_updated()
  print("Updated  Accessibility.")
  mm_tracker_on_accessibility_updated()
  oot_tracker_on_accessibility_updated()
end

function tracker_on_pack_ready()
  print("Pack Ready!")
  -- mm_tracker_on_pack_ready()
  oot_tracker_on_pack_ready()
end
