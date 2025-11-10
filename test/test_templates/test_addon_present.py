import bpy
import json
results_dict = {}
results_dict["addons"] = []
for addon in bpy.context.preferences.addons:
    print(addon.module)
    results_dict["addons"].append(addon.module)

with open("test/blender_out.json", "w") as f:
    json.dump(results_dict, f)
print("Results written to test/blender_out.json")