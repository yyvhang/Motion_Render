import numpy as np
import json
import os
import math
import argparse
import bpy

def render_human_motion(mesh_folder, save_img_folder, scene_file):
    '''
    mesh_folder: save .ply or.obj mesh file, the file should be named by order
    save_img_folder: save the render per-frame image
    scene_file: the background .blend file   
    '''
    bpy.ops.wm.open_mainfile(filepath=scene_file)
    bpy.context.scene.render.use_persistent_data = True
    bpy.context.scene.cycles.device = "GPU"
    bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'
    bpy.context.preferences.addons["cycles"].preferences.get_devices()
    print(bpy.context.preferences.addons["cycles"].preferences.compute_device_type)

    for d in bpy.context.preferences.addons["cycles"].preferences.devices:
        d["use"] = 1 # Using all devices, include GPU and CPU
        print(d["name"], d["use"])

    if not os.path.exists(save_img_folder):
        os.makedirs(save_img_folder)

    ori_obj_files = os.listdir(mesh_folder)
    ori_obj_files.sort()
    obj_files = []
    for tmp_name in ori_obj_files:
        if ".obj" in tmp_name or ".ply" in tmp_name:
            obj_files.append(tmp_name)

    for frame_idx in range(len(obj_files)):
        file_name = obj_files[frame_idx]

        # Iterate folder to process all model
        path_to_file = os.path.join(mesh_folder, file_name)

        # Load human mesh and set material 
        if ".obj" in path_to_file:
            human_new_obj = bpy.ops.import_scene.obj(filepath=path_to_file, split_mode ="OFF")
        elif ".ply" in path_to_file:
            human_new_obj = bpy.ops.import_mesh.ply(filepath=path_to_file)

        human_obj_object = bpy.data.objects[str(file_name.replace(".ply", "").replace(".obj", ""))]
        # obj_object.scale = (0.3, 0.3, 0.3)
        human_mesh = human_obj_object.data
        for f in human_mesh.polygons:
            f.use_smooth = True

        human_obj_object.rotation_euler = (math.radians(0), math.radians(0), math.radians(0)) # The default seems 90, 0, 0 while importing .obj into blender 
        # obj_object.location.y = 0

        human_mat = bpy.data.materials.new(name="MaterialName")  # set new material to variable
        human_obj_object.data.materials.append(human_mat)
        human_mat.use_nodes = True
        principled_bsdf = human_mat.node_tree.nodes['Principled BSDF']
        if principled_bsdf is not None:
            # principled_bsdf.inputs[0].default_value = (220/255.0, 220/255.0, 220/255.0, 1) # Gray, close to white after rendering 
            principled_bsdf.inputs[0].default_value = (10/255.0, 30/255.0, 225/255.0, 1) # Light Blue, used for floor scene 

        human_obj_object.active_material = human_mat

        bpy.data.scenes['Scene'].render.filepath = os.path.join(save_img_folder, ("%05d"%frame_idx)+".jpg")
        bpy.ops.render.render(write_still=True)

        # Delet materials
        for block in bpy.data.materials:
            if block.users == 0:
                bpy.data.materials.remove(block)

        bpy.data.objects.remove(human_obj_object, do_unlink=True)     
    bpy.ops.wm.quit_blender()

def render_hoi_motion(mesh_folder, save_img_folder, scene_file):
    '''
    mesh_folder: save .ply or.obj mesh file, including human & object mesh, obj mesh end with '_object.ply'
    save_img_folder: save the render per-frame image
    scene_file: the background .blend file   
    '''
    bpy.ops.wm.open_mainfile(filepath=scene_file)
    bpy.context.scene.render.use_persistent_data = True
    bpy.context.scene.cycles.device = "GPU"
    bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'
    bpy.context.preferences.addons["cycles"].preferences.get_devices()
    print(bpy.context.preferences.addons["cycles"].preferences.compute_device_type)

    for d in bpy.context.preferences.addons["cycles"].preferences.devices:
        d["use"] = 1 # Using all devices, include GPU and CPU
        print(d["name"], d["use"])

    if not os.path.exists(save_img_folder):
        os.makedirs(save_img_folder)

    ori_obj_files = os.listdir(mesh_folder)
    ori_obj_files.sort()
    obj_files = []
    for tmp_name in ori_obj_files:
        if ".obj" in tmp_name or ".ply" in tmp_name and "object" not in tmp_name:
            obj_files.append(tmp_name)

    for frame_idx in range(len(obj_files)):
        file_name = obj_files[frame_idx]

        # Iterate folder to process all model
        path_to_file = os.path.join(mesh_folder, file_name)
        object_path_to_file = path_to_file.replace(".ply", "_object.ply").replace(".obj", "_object.obj")
        # Load human mesh and set material 
        if ".obj" in path_to_file:
            human_new_obj = bpy.ops.import_scene.obj(filepath=path_to_file, split_mode ="OFF")
        elif ".ply" in path_to_file:
            human_new_obj = bpy.ops.import_mesh.ply(filepath=path_to_file)

        human_obj_object = bpy.data.objects[str(file_name.replace(".ply", "").replace(".obj", ""))]
        # obj_object.scale = (0.3, 0.3, 0.3)
        human_mesh = human_obj_object.data
        for f in human_mesh.polygons:
            f.use_smooth = True

        human_obj_object.rotation_euler = (math.radians(0), math.radians(0), math.radians(0)) # The default seems 90, 0, 0 while importing .obj into blender 
        # obj_object.location.y = 0

        human_mat = bpy.data.materials.new(name="MaterialName")  # set new material to variable
        human_obj_object.data.materials.append(human_mat)
        human_mat.use_nodes = True
        principled_bsdf = human_mat.node_tree.nodes['Principled BSDF']
        if principled_bsdf is not None:
            # principled_bsdf.inputs[0].default_value = (220/255.0, 220/255.0, 220/255.0, 1) # Gray, close to white after rendering 
            principled_bsdf.inputs[0].default_value = (10/255.0, 30/255.0, 225/255.0, 1) # Light Blue, used for floor scene 

        human_obj_object.active_material = human_mat

        # Load object mesh and set material 
        if ".obj" in object_path_to_file:
            new_obj = bpy.ops.import_scene.obj(filepath=object_path_to_file, split_mode ="OFF")
        elif ".ply" in path_to_file:
            new_obj = bpy.ops.import_mesh.ply(filepath=object_path_to_file)
        # obj_object = bpy.context.selected_objects[0]
        obj_object = bpy.data.objects[str(file_name.replace(".ply", "").replace(".obj", "")+"_object")]
        # obj_object.scale = (0.3, 0.3, 0.3)
        mesh = obj_object.data
        for f in mesh.polygons:
            f.use_smooth = True
        
        obj_object.rotation_euler = (math.radians(0), math.radians(0), math.radians(0)) # The default seems 90, 0, 0 while importing .obj into blender 
        # obj_object.location.y = 0

        mat = bpy.data.materials.new(name="MaterialName")  # set new material to variable
        obj_object.data.materials.append(mat)
        mat.use_nodes = True
        principled_bsdf = mat.node_tree.nodes['Principled BSDF']
        if principled_bsdf is not None:
            # principled_bsdf.inputs[0].default_value = (220/255.0, 220/255.0, 220/255.0, 1) # Gray, close to white after rendering 
            # principled_bsdf.inputs[0].default_value = (10/255.0, 30/255.0, 225/255.0, 1) # Light Blue, used for floor scene 
            principled_bsdf.inputs[0].default_value = (153/255.0, 51/255.0, 255/255.0, 1) # Light Purple

        obj_object.active_material = mat

        bpy.data.scenes['Scene'].render.filepath = os.path.join(save_img_folder, ("%05d"%frame_idx)+".jpg")
        bpy.ops.render.render(write_still=True)

        # Delet materials
        for block in bpy.data.materials:
            if block.users == 0:
                bpy.data.materials.remove(block)

        bpy.data.objects.remove(human_obj_object, do_unlink=True)
        bpy.data.objects.remove(obj_object, do_unlink=True)
    bpy.ops.wm.quit_blender()

if __name__=='__main__':
    import sys
    argv = sys.argv

    if "--" not in argv:
        argv = []
    else:
        argv = argv[argv.index("--")+1:]

    print("argsv:{0}".format(argv))
    parser = argparse.ArgumentParser(description='Render Motion in 3D Environment.')
    parser.add_argument('--folder', type=str, metavar='PATH',
                        help='path to specific folder which include folders containing .obj files',
                        default='')
    parser.add_argument('--out_folder', type=str, metavar='PATH',
                        help='path to output folder which include rendered img files',
                        default='')
    parser.add_argument('--scene', type=str, metavar='PATH',
                        help='path to specific .blend path for 3D scene',
                        default='floor_colorful_mat.blend')
    parser.add_argument('--mode', type=str, default='hoi',
                        help='render mode: human or hoi')
    args = parser.parse_args(argv)
    if args.mode == 'hoi':
        render_hoi_motion(args.folder, args.out_folder, args.scene)
    elif args.mode == 'human':
        render_human_motion(args.folder, args.out_folder, args.scene)


    '''
    run:
    blender -P render_motion.py -b -- --folder --scene --out_folder --out_video, shell=True
    '''