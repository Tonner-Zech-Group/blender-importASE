import bpy
import sys
import json

results_dict = {}
results_dict["blender_version"] = bpy.app.version
results_dict["python_version"] = sys.version
results_dict["objects"] = [obj.name for obj in bpy.context.scene.objects]

with open("test/blender_out.json", "w") as f:
    json.dump(results_dict, f)
print("Results written to test/blender_out.json")
