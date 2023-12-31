## Render by blender and use self-made background
This is refered to [OMOMO](https://github.com/lijiaman/omomo_release), 'floor_colorful_mat.blend' is the self-made background file, you can modify it in Blender, e.g. set the camera view and change the light. You can see the rendered motion in `demo_hoi.mp4` and `demo_human.mp4`.

To make the render, run the following command:
```
bash render_motion.sh
```
* `--folder` is the folder which contains `.ply` files (SMPL human or object mesh) to be rendered; 
* `--scene` is the path for background `.blender` file; 
* `--out_folder` is the path to save the rendered image;
* `--mode` could chose to render hoi or just human motion;
* `--out_video` is the output video path;
* `--reaxis` is used to adapt the xyz axis in Blender software;