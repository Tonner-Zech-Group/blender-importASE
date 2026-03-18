
import bpy
from blender_importASE.ui import import_ase_molecule
import os
print("Importing modules completed.")

filepath = "###STRUCTURE###"  # Placeholder to be replaced in the test
colorbonds = ("###COLORBONDS###" == True)  # Placeholder to be replaced in the test
color = float("###COLOR###")  # Placeholder to be replaced in the test
long_bonds = ("###LONG_BONDS###" == True)  # Placeholder to be replaced in the test
scale = float("###SCALE###")  # Placeholder to be replaced in the test
unit_cell = ("###UNIT_CELL###" == True)  # Placeholder to be replaced in the test
representation = "###REPRESENTATION###"  # Placeholder to be replaced in the test
read_density = ("###READ_DENSITY###" == True)  # Placeholder to be replaced in the test
zero_cell = ("###ZERO_CELL###" == True)  # Placeholder to be replaced in the test
outline = ("###OUTLINE###" == True)  # Placeholder to be replaced in the test
imageslice = ("###IMAGE_SLICE###" == True)  # Placeholder to be replaced in the test
animate = ("###ANIMATE###" == True)  # Placeholder to be replaced in the test
overwrite = ("###OVERWRITE###" == True)  # Placeholder to be replaced in the test
resolution = int("###RESOLUTION###")  # Placeholder to be replaced in the test
name = os.path.basename(filepath)
render = ("###RENDER###" == True)  # Placeholder to be replaced in the test


import_ase_molecule(filepath, name,
                                resolution=32,
                                color=color, colorbonds=colorbonds, long_bonds=long_bonds, scale=scale,
                                unit_cell=unit_cell, representation=representation,
                                read_density=read_density, 
                                shift_cell=zero_cell, imageslice=imageslice,
                                animate=animate, outline=outline,
                                overwrite=overwrite, add_supercell=True
                                )

out_dict = {}
out_dict["objects"] = [obj.name for obj in bpy.data.objects if obj.type == "MESH"]
out_dict["materials"] = [mat.name for mat in bpy.data.materials]
out_dict["modifier_list"] = []
for ob in out_dict["objects"]:
    md_list = []
    obj = bpy.data.objects[ob]
    modifiers = obj.modifiers
    for mod in modifiers:
        md_list.append(mod.name)
    out_dict["modifier_list"].append(md_list)

if render:
    