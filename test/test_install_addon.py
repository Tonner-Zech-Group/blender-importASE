import bpy
import os
from importlib.metadata import packages_distributions

addon_path = "###ADDON_PATH###"  # Placeholder to be replaced in the test
results_dict = {}

# Install the addon
bpy.ops.preferences.addon_install(filepath=addon_path, overwrite=True, enable_on_install=True)

# Check if the addon is enabled
addon_enabled = False
for addon in bpy.context.preferences.addons:
    if addon.module == "blender_importASE":
        addon_enabled = True
        break
results_dict["addon_enabled"] = addon_enabled
results_dict["modules"] = list(packages_distributions().keys())

with open("blender_out.json", "w") as f:
    import json
    json.dump(results_dict, f)
    