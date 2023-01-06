import argparse
import os
import sys
from ast import List

import bpy
import numpy as np

ROOT_PATH = r"F:\MyPython\blender"
sys.path += [ROOT_PATH, os.path.join(ROOT_PATH, "utils")]
from utils.bpy_utils import (clear_scene, duplicate_object, import_object,
                             initialize_camera, render, save_proj, create_light, create_plane, create_material)
from utils.utils import rename_by_timestamp


def create_material_mirror():
    mirror_mat = create_material()
    mirror_mat.name = "mirror"
    mirror_mat.node_tree.nodes["Principled BSDF"].inputs[6].default_value = 1  # metallic
    mirror_mat.node_tree.nodes["Principled BSDF"].inputs[9].default_value = 0  # roughness



def initialize_monkey():
    bpy.ops.mesh.primitive_monkey_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    obj = bpy.data.objects[-1]
    obj.scale = [0.5, 0.5, 0.5]
    obj.location.z = 0.15


def initialize_light():
    light_obj = create_light()
    # light_obj = bpy.data.objects["Spot"]
    light_obj.location = [0, 2.72, 5]
    light_obj.rotation_euler = [-0.54, 0, 0]
    
    light = bpy.data.lights[light_obj.name]
    light.color = [1.0, 0.58, 0.21]
    light.energy = 500


def initialize_mirror():
    plane_obj = create_plane()
    plane_obj.location = [0, 0, -3]
    plane_obj.scale = [10, 10, 1]

    mirror_mat = bpy.data.materials["mirror"]
    plane_obj.data.materials.append(mirror_mat)





def initialize_dss_crystals(file_path: str = os.path.join(ROOT_PATH, "Asset\Gem\DSS_v1.blend"), num: int = 12):
    """Put 12 DSS crystals at initial postures."""
    prototype_obj = import_object(file_path=file_path, object_name="DSS")
    print(f"prototype_obj: {prototype_obj}")
    
    obj_list = []
    for i in range(num):
        # duplicate
        cur_obj = duplicate_object()
        # set properties
        cur_obj.name = f"DSS_crystal - {i:03d}"
        cur_yaw = i / num * 2 * np.pi
        cur_obj.location = [np.cos(cur_yaw), np.sin(cur_yaw), 0]
        cur_obj.rotation_euler = [0, 0, cur_yaw]
        # append for return
        obj_list.append(cur_obj)

    bpy.data.objects.remove(prototype_obj)

    return obj_list


def stage1(obj_list, t_total, d_yaw_total = 2 * np.pi, d_roll_total = 16 * np.pi):
    for obj in obj_list:
        x, y, _ = list(obj.location)
        roll, _, yaw = list(obj.rotation_euler)
        for t_idx in range(t_total):
            d_yaw = t_idx / t_total * d_yaw_total
            d_roll = t_idx / t_total * d_roll_total
            # x, y = obj.location.x, obj.location.y
            obj.location.x = np.cos(d_yaw) * x - np.sin(d_yaw) * y
            obj.location.y = np.sin(d_yaw) * x + np.cos(d_yaw) * y        
            obj.keyframe_insert(data_path="location", frame=t_idx)
            obj.rotation_euler.x = roll + d_roll
            obj.rotation_euler.z = yaw + d_yaw
            obj.keyframe_insert(data_path="rotation_euler", frame=t_idx)
            


def main():
    ########## CONFIG ##########
    exp_name = "DSS_v0"
    img_dir = os.path.join(r"F:\MyPython\blender\rendered", exp_name)
    img_dir = rename_by_timestamp(img_dir, is_file=False)

    proj_file = os.path.join(r"F:\MyPython\blender\projs", exp_name+".blend")
    proj_file = rename_by_timestamp(proj_file, is_file=True)
    
    # frame_num = 600
    frame_num = 240
    # frame_num = 15
    # frame_num = 1


    ########## MATERIAL ##########
    create_material_mirror()


    ########## OBJECT ##########
    clear_scene()

    cam = initialize_camera(
        cam_pose=[3.7, -3.5, 2.5, 1.109, 0.0, 0.815], 
        lens=50
    )
    
    initialize_monkey()    
    obj_list = initialize_dss_crystals(num=12)
    initialize_mirror()


    ########## LIGHT ##########
    initialize_light()

    
    

    ########## ANIME ##########
    stage1(obj_list, frame_num)


    # ########## RENDER ##########
    # obj = obj_list[0]
    # fc = obj.animation_data.action.fcurves[0]
    # for k in fc.keyframe_points:
    #     t= int(k.co[0])
    #     img_path = os.path.join(img_dir, f"frame_{t:04d}.exr")
    #     bpy.context.scene.frame_set(t)
    #     bpy.context.view_layer.update()
    #     render(cam, img_path, pref="fast")



    ########## SAVE ##########
    save_proj(save_path=proj_file)


if __name__ == "__main__":
    main()
