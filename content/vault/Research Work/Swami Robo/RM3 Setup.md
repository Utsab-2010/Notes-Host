---
title: "RM3 Setup"
lastmod: 2026-06-26
---

For metaworld environments, install the environments by cloning this [fork of the metaworld repo](https://github.com/suraj-nair-1/metaworld) and installing via `pip install -e .`
 - Your build will fail probs.
 - Install mujoco200 into the ~/.mujoco/mujoco200 folder (refer to link below)
	 - [Install MuJoCo 200 & 210 on Linux · GitHub](https://gist.github.com/ellisbrown/47bfd3e524aed11216cd3c0a0872a654)
 - rename paths properly
   ```bash
   export MUJOCO_PY_MUJOCO_PATH=~/.mujoco/mujoco200
   export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/.mujoco/mujoco200/bin
   ```
   
- If still fails , degrade cython `pip install "cython == 0.29.37" `
- The gym and metaworld builds properly. mujoco wheel might still fail. Check the error message  - for me I was missing the following package.
	- sudo apt install libosmesa6-dev libgl1-mesa-glx libglfw3
- Also use `pip install -e . --no-build-isolation` instead