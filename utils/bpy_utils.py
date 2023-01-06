import os
import bpy
# from utils import rename_by_timestamp


def clear_scene():
    for obj in bpy.data.objects:
        bpy.data.objects.remove(obj)


def initialize_camera(cam_pose: list, lens: float = 50):
    """
    Return: a blender camera
    """
    loc = cam_pose[0:3]
    rot = cam_pose[3:6]
    bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=loc, rotation=rot, scale=(1, 1, 1))
    cur_cam = bpy.data.cameras[0]
    cur_cam.lens = lens
    return cur_cam


def render(cam, img_path, pref="fast", write_still=True, animation=False):
    """
    Params:
        cam:        a blender camera or blender object with correct name.
        img_path:   detailed path, like `F:\MyPython\blender\rendered\animate01-Dec 17 13-50-41\frame_0000.png`
    """
    # render settings
    bpy.data.scenes[0].render.engine = "CYCLES"
    bpy.context.scene.cycles.device = 'GPU'
    if pref == "good":
        bpy.context.scene.cycles.samples = 4096
        bpy.context.scene.cycles.time_limit = 60
    elif pref == "fast":
        bpy.context.scene.cycles.samples = 256
        bpy.context.scene.cycles.time_limit = 10
    elif pref == "very_fast":
        bpy.context.scene.cycles.samples = 16
        bpy.context.scene.cycles.time_limit = 1
    else:
        print(f"[WARNING] invalid render preference: `{pref}`. Using `fast` instead.")
        render(cam, img_path, pref="fast")

    bpy.data.scenes['Scene'].camera = bpy.data.objects[cam.name]
    bpy.context.scene.render.filepath = img_path

    # do rendering
    bpy.ops.render.render(write_still=write_still, animation=animation)


def save_proj(save_path:str):
    """
    Params:
        save_path:  `F:\\MyPython\\blender\\projs\\animate01-Jan 2 21-52-13.blend`.
    """
    save_dir, file_name = save_path.rsplit(os.path.sep, maxsplit=1)
    os.makedirs(save_dir, exist_ok=True)
    # rename save_path in case already exist such file
    if os.path.exists(save_path):
        save_path = utils.rename_by_timestamp(save_path, is_file=True)
    print("Save to: ", save_path)
    bpy.ops.wm.save_as_mainfile(filepath=save_path)


def result_obj(func, *args, **kwargs):
    """Decorator for returning the **ONLY** newly appended object."""
    def foo(*args, **kwargs):
        prev_objs = set(list(bpy.data.objects))
        
        func(*args, **kwargs)

        next_objs = set(list(bpy.data.objects))
        cur_obj = next_objs - prev_objs
        assert len(cur_obj) == 1, f"Detected {len(cur_obj)} new objects, expect 1."
        return cur_obj.pop()
    return foo


@result_obj
def import_object(file_path, object_name="DSS"):
    """
    Params:
    
    Return: the imported object.
    """

    inner_path = 'Object'
    bpy.ops.wm.append(
        filepath=os.path.join(file_path, inner_path, object_name),
        directory=os.path.join(file_path, inner_path),
        filename=object_name
    )

@result_obj
def duplicate_object():
    bpy.ops.object.duplicate_move()


@result_obj
def create_light():
    bpy.ops.object.light_add(
        type='SPOT', 
        # align='WORLD', 
        location=(0, 0, 0), 
        # scale=(1, 1, 1)
    )

@result_obj
def create_plane():
    bpy.ops.mesh.primitive_plane_add(
        # enter_editmode=False, 
        # align='WORLD', 
        # location=(0, 0, -3), 
        # scale=(10, 10, 1)
    )






def result_mat(func, *args, **kwargs):
    """Decorator for returning the **ONLY** newly appended material."""
    def foo(*args, **kwargs):
        prev_mats = set(list(bpy.data.materials))
        
        func(*args, **kwargs)

        next_mats = set(list(bpy.data.materials))
        cur_mat = next_mats - prev_mats
        assert len(cur_mat) == 1, f"Detected {len(cur_mat)} new objects, expect 1."
        return cur_mat.pop()
    return foo

@result_mat
def create_material():
    bpy.ops.material.new()