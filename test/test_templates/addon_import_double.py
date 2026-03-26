import json
import os

import bpy
from blender_importASE.ui import import_ase_molecule

print("Importing modules completed.")

filepath = "###STRUCTURE###"
name = os.path.basename(filepath)
colorbonds = ("###COLORBONDS###" == "True")
color = float("###COLOR###")
long_bonds = ("###LONG_BONDS###" == "True")
scale = float("###SCALE###")
unit_cell = ("###UNIT_CELL###" == "True")
representation = "###REPRESENTATION###"
read_density = ("###READ_DENSITY###" == "True")
zero_cell = ("###ZERO_CELL###" == "True")
outline = ("###OUTLINE###" == "True")
imageslice = 1
animate = ("###ANIMATE###" == "True")
resolution = int("###RESOLUTION###")

# First import
import_ase_molecule(
    filepath, name,
    resolution=resolution,
    color=color, colorbonds=colorbonds, long_bonds=long_bonds, scale=scale,
    unit_cell=unit_cell, representation=representation,
    read_density=read_density,
    shift_cell=zero_cell,
    animate=animate, outline=outline,
    overwrite=False, add_supercell=False,
)

objects_after_first = [obj.name for obj in bpy.data.objects if obj.type == "MESH"]

# Second import — same file, overwrite=False so a new collection is created
import_ase_molecule(
    filepath, name,
    resolution=resolution,
    color=color, colorbonds=colorbonds, long_bonds=long_bonds, scale=scale,
    unit_cell=unit_cell, representation=representation,
    read_density=read_density,
    shift_cell=zero_cell,
    animate=animate, outline=outline,
    overwrite=False, add_supercell=False,
)

objects_after_second = [obj.name for obj in bpy.data.objects if obj.type == "MESH"]

out_dict = {
    "objects_after_first": objects_after_first,
    "objects_after_second": objects_after_second,
    "materials": [mat.name for mat in bpy.data.materials],
    "collections": [col.name for col in bpy.data.collections],
}

with open("test/blender_out.json", "w") as f:
    json.dump(out_dict, f)
print("Results written to test/blender_out.json")
