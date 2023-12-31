import imageio
import argparse
import subprocess 
import os
import numpy as np
import open3d as o3d

def images_to_video_w_imageio(img_folder, output_vid_file):
    img_files = os.listdir(img_folder)
    img_files.sort()
    im_arr = []
    for img_name in img_files:
        img_path = os.path.join(img_folder, img_name)
        im = imageio.imread(img_path)
        im_arr.append(im)

    im_arr = np.asarray(im_arr)
    imageio.mimwrite(output_vid_file, im_arr, fps=30, quality=8)

def re_axis_mesh(folder):
    Vector3dVector = o3d.utility.Vector3dVector
    files = os.listdir(folder)
    for file in files:
        if ".ply" in file:
            mesh_file = os.path.join(folder, file)
            mesh = o3d.io.read_triangle_mesh(mesh_file)
            vertex = np.array(mesh.vertices)
            vertex[:, 1], vertex[:, 2] = -vertex[:, 2].copy(), vertex[:, 1].copy()
            mesh.vertices = Vector3dVector(vertex)
            o3d.io.write_triangle_mesh(mesh_file, mesh)

if __name__=='__main__':
    import sys
    import pdb
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
                        default='')
    parser.add_argument('--mode', type=str, default='hoi',
                        help='render mode: human or hoi')
    parser.add_argument('--out_video', type=str, default='',
                        help='path to save render video')
    parser.add_argument('--reaxis', type=bool, default='True',
                        help='whether to re axis')
    args = parser.parse_args()

    blender_py_path = "blender_render.py"
    folder = args.folder
    scene = args.scene
    out_folder = args.out_folder
    mode = args.mode

    #if need re_axis
    if args.reaxis:
        re_axis_mesh(folder)
    subprocess.call("blender"+" -P "+blender_py_path+" -b -- --folder "+folder+" --scene "+scene+" --out_folder "+out_folder+" --mode "+mode, shell=True)
    images_to_video_w_imageio(args.out_folder, args.out_video)