## Render by Blender without background
This is referred to [MLD](https://github.com/ChenFengYe/motion-latent-diffusion ). You can see the rendered motion in demo.mp4.
If you just got the joint like `(n, 22, 3)`, `n` is the frames, run `fit_fast.py` or `fit.py` to get the human mesh:
```
python -m fit --dir YOUR_NPY_FOLDER --save_folder TEMP_PLY_FOLDER --cuda
```
`fit.py` use the pre-frame to optimize the SMPL, `fit_fast.py` use the T-pose for each frame. \
Then, you can run the following command to render the motion:
```
bash render.sh
```
* you can change default render settings in `render.yaml`;
* `--dir` is folder which contains `.npy` files ready to be rendered;
