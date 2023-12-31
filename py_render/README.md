## Render by pyrender
This is refered to [T2M-GPT](https://github.com/Mael-zys/T2M-GPT), you can see the rendered motion in `demo.gif`. \
Run the following command to render the motion:
```
python render.py --filedir motion_folder --motion-list file_name
```
* `--filedir` is the folder which contains the `.npy` files;
* `--motion-list` is the file_name, e.g. the file is `01234.npy`, then you should input `01234`;
* You should modify the path of SMPL in `visualize/joints2smpl/src/config.py`;