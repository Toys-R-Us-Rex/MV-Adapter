### 

## Don't build

[Dockerfile v2](Dockerfile.v2)

<details>
<summary>Result</summary>

```bash
[+] Building 7.7s (13/14)                                                                                                                                                                                                                                                                                        docker:default
 => [internal] load build definition from backup_Dockerfile                                                                                                                                                                                                                                                                0.0s
 => => transferring dockerfile: 1.34kB                                                                                                                                                                                                                                                                                     0.0s
 => [internal] load metadata for docker.io/nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04                                                                                                                                                                                                                                     0.8s
 => [internal] load .dockerignore                                                                                                                                                                                                                                                                                          0.0s
 => => transferring context: 2B                                                                                                                                                                                                                                                                                            0.0s
 => [ 1/10] FROM docker.io/nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04@sha256:8f9dd0d09d3ad3900357a1cf7f887888b5b74056636cd6ef03c160c3cd4b1d95                                                                                                                                                                             0.0s
 => [internal] load build context                                                                                                                                                                                                                                                                                          0.0s
 => => transferring context: 9.69kB                                                                                                                                                                                                                                                                                        0.0s
 => CACHED [ 2/10] RUN apt-get update && apt-get install -y     python3.10     python3.10-dev     python3-pip     git     wget     curl     libgl1-mesa-glx     libglib2.0-0     libsm6     libxrender1     libxext6     && rm -rf /var/lib/apt/lists/*                                                                    0.0s
 => CACHED [ 3/10] RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1 &&     update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1                                                                                                                                                    0.0s
 => CACHED [ 4/10] RUN pip install --upgrade pip                                                                                                                                                                                                                                                                           0.0s
 => CACHED [ 5/10] RUN pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118                                                                                                                                                                                                                    0.0s
 => CACHED [ 6/10] RUN pip install --no-build-isolation git+https://github.com/NVlabs/nvdiffrast.git                                                                                                                                                                                                                       0.0s
 => CACHED [ 7/10] WORKDIR /workspace                                                                                                                                                                                                                                                                                      0.0s
 => [ 8/10] COPY . .                                                                                                                                                                                                                                                                                                       0.1s
 => ERROR [ 9/10] RUN pip install -r requirements.txt                                                                                                                                                                                                                                                                      5.6s
------                                                                                                                                                                                                                                                                                                                          
 > [ 9/10] RUN pip install -r requirements.txt:                                                                                                                                                                                                                                                                                 
0.689 Collecting git+https://github.com/NVlabs/nvdiffrast.git (from -r requirements.txt (line 19))                                                                                                                                                                                                                              
0.689   Cloning https://github.com/NVlabs/nvdiffrast.git to /tmp/pip-req-build-bimu3_71                                                                                                                                                                                                                                         
0.693   Running command git clone --filter=blob:none --quiet https://github.com/NVlabs/nvdiffrast.git /tmp/pip-req-build-bimu3_71                                                                                                                                                                                               
2.434   Resolved https://github.com/NVlabs/nvdiffrast.git to commit 253ac4fcea7de5f396371124af597e6cc957bfae                                                                                                                                                                                                                    
2.441   Installing build dependencies: started
4.526   Installing build dependencies: finished with status 'done'
4.530   Getting requirements to build wheel: started
4.840   Getting requirements to build wheel: finished with status 'error'
4.852   error: subprocess-exited-with-error
4.852   
4.852   × Getting requirements to build wheel did not run successfully.
4.852   │ exit code: 1
4.852   ╰─> [10 lines of output]
4.852       
4.852       
4.852       **********************************************************************
4.852       ERROR! Cannot compile nvdiffrast CUDA extension. Please ensure that:
4.852       
4.852       1. You have PyTorch installed
4.852       2. You run 'pip install' with --no-build-isolation flag
4.852       **********************************************************************
4.852       
4.852       
4.852       [end of output]
4.852   
4.852   note: This error originates from a subprocess, and is likely not a problem with pip.
4.856 ERROR: Failed to build 'git+https://github.com/NVlabs/nvdiffrast.git' when getting requirements to build wheel
------
backup_Dockerfile:43
--------------------
  41 |     
  42 |     # Install Python dependencies
  43 | >>> RUN pip install -r requirements.txt
  44 |     
  45 |     # Create output directory
--------------------
ERROR: failed to build: failed to solve: process "/bin/sh -c pip install -r requirements.txt" did not complete successfully: exit code: 1
```

</details>

---

[Dockerfile v3](Dockerfile.v3)

<details>
<summary>Result</summary>

```bash
[+] Building 8.1s (13/13) FINISHED                                                                                                                       docker:default
 => [internal] load build definition from backup_Dockerfile3                                                                                                       0.0s
 => => transferring dockerfile: 1.32kB                                                                                                                             0.0s
 => [internal] load metadata for docker.io/nvidia/cuda:12.1.1-devel-ubuntu22.04                                                                                    0.4s
 => [internal] load .dockerignore                                                                                                                                  0.0s
 => => transferring context: 2B                                                                                                                                    0.0s
 => [internal] load build context                                                                                                                                  0.0s
 => => transferring context: 9.68kB                                                                                                                                0.0s
 => [1/9] FROM docker.io/nvidia/cuda:12.1.1-devel-ubuntu22.04@sha256:7012e535a47883527d402da998384c30b936140c05e2537158c80b8143ee7425                              0.0s
 => CACHED [2/9] RUN apt-get update && apt-get install -y --no-install-recommends     python3.10     python3-pip     python3-dev     git     ninja-build     libg  0.0s
 => CACHED [3/9] RUN ln -s /usr/bin/python3.10 /usr/bin/python                                                                                                     0.0s
 => CACHED [4/9] WORKDIR /workspace                                                                                                                                0.0s
 => CACHED [5/9] RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cu121                                               0.0s
 => CACHED [6/9] RUN pip install --no-cache-dir setuptools wheel                                                                                                   0.0s
 => CACHED [7/9] RUN git clone https://github.com/NVlabs/nvdiffrast.git /tmp/nvdiffrast &&     cd /tmp/nvdiffrast &&     pip install --no-build-isolation . &&     0.0s
 => [8/9] COPY . .                                                                                                                                                 0.2s
 => ERROR [9/9] RUN pip install --no-cache-dir -r requirements.txt                                                                                                 7.4s
------                                                                                                                                                                  
 > [9/9] RUN pip install --no-cache-dir -r requirements.txt:                                                                                                            
0.887 Collecting git+https://github.com/NVlabs/nvdiffrast.git (from -r requirements.txt (line 19))                                                                      
0.888   Cloning https://github.com/NVlabs/nvdiffrast.git to /tmp/pip-req-build-sy5th5dr                                                                                 
0.892   Running command git clone --filter=blob:none --quiet https://github.com/NVlabs/nvdiffrast.git /tmp/pip-req-build-sy5th5dr                                       
2.862   Resolved https://github.com/NVlabs/nvdiffrast.git to commit 253ac4fcea7de5f396371124af597e6cc957bfae                                                            
3.116   Installing build dependencies: started
7.003   Installing build dependencies: finished with status 'done'
7.011   Getting requirements to build wheel: started
7.196   Getting requirements to build wheel: finished with status 'error'
7.208   error: subprocess-exited-with-error
7.208   
7.208   × Getting requirements to build wheel did not run successfully.
7.208   │ exit code: 1
7.208   ╰─> [10 lines of output]
7.208       
7.208       
7.208       **********************************************************************
7.208       ERROR! Cannot compile nvdiffrast CUDA extension. Please ensure that:
7.208       
7.208       1. You have PyTorch installed
7.208       2. You run 'pip install' with --no-build-isolation flag
7.208       **********************************************************************
7.208       
7.208       
7.208       [end of output]
7.208   
7.208   note: This error originates from a subprocess, and is likely not a problem with pip.
7.212 error: subprocess-exited-with-error
7.212 
7.212 × Getting requirements to build wheel did not run successfully.
7.212 │ exit code: 1
7.212 ╰─> See above for output.
7.212 
7.212 note: This error originates from a subprocess, and is likely not a problem with pip.
------
backup_Dockerfile3:41
--------------------
  39 |     # 3. FIX: Install requirements with --no-build-isolation
  40 |     # This allows nvdiffrast to use the PyTorch we just installed to compile its kernels
  41 | >>> RUN pip install --no-cache-dir -r requirements.txt
  42 |     
  43 |     EXPOSE 7860
--------------------
ERROR: failed to build: failed to solve: process "/bin/sh -c pip install --no-cache-dir -r requirements.txt" did not complete successfully: exit code: 1
```

</details>

## Don't run

[Dockerfile v1](Dockerfile.v1)

<details>
<summary>Result</summary>

```bash
==========
== CUDA ==
==========

CUDA Version 12.1.1

Container image Copyright (c) 2016-2023, NVIDIA CORPORATION & AFFILIATES. All rights reserved.

This container image and its contents are governed by the NVIDIA Deep Learning Container License.
By pulling and using the container, you accept the terms and conditions of this license:
https://developer.nvidia.com/ngc/nvidia-deep-learning-container-license

A copy of this license is made available in this container at /NGC-DL-CONTAINER-LICENSE for your convenience.

root@7f1cd5fe5937:/workspace# python -m scripts.texture_i2tex \
--image assets/demo/ig2mv/1ccd5c1563ea4f5fb8152eac59dabd5c.jpeg \
--mesh assets/demo/ig2mv/1ccd5c1563ea4f5fb8152eac59dabd5c.glb \
--save_dir outputs --save_name i2tex_sample \
--remove_bg
Traceback (most recent call last):
  File "/opt/conda/lib/python3.9/runpy.py", line 197, in _run_module_as_main
    return _run_code(code, main_globals, None,
  File "/opt/conda/lib/python3.9/runpy.py", line 87, in _run_code
    exec(code, run_globals)
  File "/workspace/scripts/texture_i2tex.py", line 9, in <module>
    from mvadapter.pipelines.pipeline_texture import ModProcessConfig, TexturePipeline
  File "/workspace/mvadapter/pipelines/pipeline_texture.py", line 12, in <module>
    from mvadapter.utils import image_to_tensor, make_image_grid, tensor_to_image
  File "/workspace/mvadapter/utils/__init__.py", line 1, in <module>
    from .mesh_utils.camera import get_camera, get_orthogonal_camera
  File "/workspace/mvadapter/utils/mesh_utils/__init__.py", line 1, in <module>
    from .camera import (
  File "/workspace/mvadapter/utils/mesh_utils/camera.py", line 12, in <module>
    from .utils import LIST_TYPE
  File "/workspace/mvadapter/utils/mesh_utils/utils.py", line 10, in <module>
    import nvdiffrast.torch as dr
  File "/opt/conda/lib/python3.9/site-packages/nvdiffrast/torch/__init__.py", line 9, in <module>
    from .ops import RasterizeCudaContext, get_log_level, set_log_level, rasterize, DepthPeeler, interpolate, texture, texture_construct_mip, antialias, antialias_construct_topology_hash, RasterizeGLContext
  File "/opt/conda/lib/python3.9/site-packages/nvdiffrast/torch/ops.py", line 12, in <module>
    import _nvdiffrast_c
ImportError: /opt/conda/lib/python3.9/site-packages/_nvdiffrast_c.cpython-39-x86_64-linux-gnu.so: undefined symbol: _ZNSt15__exception_ptr13exception_ptr9_M_addrefEv
```

</details>