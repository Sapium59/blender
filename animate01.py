import argparse
from ast import List
import os
import sys

import bpy
import numpy as np

sys.path.append(r"F:\MyPython\blender")
from utils.bpy_utils import clear_scene, save_proj, render, initialize_camera
from utils.utils import compute_rgba_from_percentage, rename_by_timestamp


def initialize_objects(cube_num: int):
    obj_list = []
    for i in range(cube_num):
        bpy.ops.mesh.primitive_cube_add(size=0.5, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        cur_obj = bpy.context.active_object
        cur_obj.name = f"Cube - {i:03d}"

        bpy.ops.material.new()
        cur_mat = bpy.data.materials[-1]
        cur_mat.name = f"Material - {i:03d}"
        cur_mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = compute_rgba_from_percentage(i / cube_num)
        cur_obj.data.materials.append(cur_mat)

        obj_list.append(cur_obj)

    return obj_list





def update_cubes_stage1(
    percentage: float, 
    obj_list: List[bpy.types.Object], 
    total_radios: float = 5, 
    total_altitude: float = 2, 
    total_publ_rot: float = 2*np.pi, 
    total_priv_rot: float = -5*np.pi, 
    dst_scale: float = 0.2
):
    """0 <= percentage <= 1 denotes the procedure."""
    def _radios_func(x, a=0.2):
        """Mysterious function to modify procedure percentrage ~ """
        return np.power(np.sin(x * np.pi / 2), a)
    radios = 1 * (1 - _radios_func(percentage)) + total_radios * _radios_func(percentage)
    altitude = total_altitude * percentage
    publ_rot = total_publ_rot * percentage
    priv_rot = total_priv_rot * percentage 
    src_scale = 0
    scale = (dst_scale - src_scale) * percentage + src_scale
    
    cube_num = len(obj_list)
    for cube_idx, cube in enumerate(obj_list):
        base_rot = 2 * np.pi * cube_idx / cube_num
        
        # location: defined by public rotation
        cur_loc = np.array([radios * np.cos(base_rot + publ_rot), radios * np.sin(base_rot + publ_rot), altitude])
        cube.location = cur_loc

        # rotation: defined by private rotation
        cur_rot = np.array([0, 0, base_rot + priv_rot])
        cube.rotation_euler = cur_rot

        # scale: self-defined
        cur_scale = [1, 1, scale]
        cube.scale = cur_scale


def update_cubes_stage2(
    percentage: float, 
    obj_list: list[bpy.types.Object], 
    total_radios: float = 5, 
    total_altitude: float = 2, 
    total_publ_rot: float = 1*np.pi, 
    total_priv_rot: float = -10*np.pi, 
    dst_scale: float = -0.2
):
    """0 <= percentage <= 1 denotes the procedure."""

    publ_rot = total_publ_rot * percentage

    cube_num = len(obj_list)
    for cube_idx, cube in enumerate(obj_list):
        base_rot = 2 * np.pi * cube_idx / cube_num
        
        # location
        prev_loc = np.array([total_radios * np.cos(base_rot + publ_rot), total_radios * np.sin(base_rot + publ_rot), total_altitude])
        next_loc = np.array([0, 0, (cube_idx / len(obj_list) - 1 / 2) * total_altitude])
        cur_loc = percentage * next_loc + (1 - percentage) * prev_loc
        cube.location = cur_loc

        # rotation
        cur_rot = np.array([0, 0, base_rot + total_priv_rot])
        cube.rotation_euler = cur_rot

        # scale: self-defined
        cur_scale = [1, 1, dst_scale]
        cube.scale = cur_scale





def main():
    exp_name = "animate01"
    img_dir = os.path.join(r"F:\MyPython\blender\rendered", exp_name)
    img_dir = rename_by_timestamp(img_dir, is_file=False)

    proj_file = os.path.join(r"F:\MyPython\blender\projs", exp_name+".blend")
    proj_file = rename_by_timestamp(proj_file, is_file=True)
    
    
    clear_scene()
    obj_list = initialize_objects(cube_num=24)
    cam = initialize_camera(cam_pose=[7.358891487121582, -6.925790786743164, 4.958309173583984, 1.1093189716339111, 0.0, 0.8149281740188599], lens=20)


    frame_num = 600
    # frame_num = 15
    frames = range(frame_num)
    for t in frames:
        img_path = os.path.join(img_dir, f"frame_{t:04d}.exr")
        update_cubes_stage1(t / frame_num, obj_list)
        bpy.context.view_layer.update()
        render(cam, img_path, pref="fast")
    
    for t in frames:
        img_path = os.path.join(img_dir, f"frame_{frame_num+t:04d}.exr")
        update_cubes_stage2(t / frame_num, obj_list)
        bpy.context.view_layer.update()
        render(cam, img_path, pref="fast")

    save_proj(save_path=proj_file)


if __name__ == "__main__":
    main()
