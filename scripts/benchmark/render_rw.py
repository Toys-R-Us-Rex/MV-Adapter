from ctypes import Array
import os
# Force offscreen OpenGL rendering.

os.environ["PYOPENGL_PLATFORM"] = "egl"
#https://stackoverflow.com/questions/38549928/off-screen-rendering-with-gpu-support-but-without-windowing-support

import argparse
# Read arguments from command line.

from pathlib import Path
# Handle file paths.

import numpy as np
# Math operations (vectors, matrices).

import pyrender
# Rendering engine.

import trimesh
# Load 3D mesh.

from PIL import Image
# Save images.


DEFAULT_IMAGE_SIZE = (1024, 1024)
DEFAULT_CAMERA_YFOV = np.pi / 3.0
DEFAULT_LIGHT_INTENSITY = 3.0
DEFAULT_RADIUS_SCALE = 2.0

#https://learnopengl.com/Getting-started/
#https://pyrender.readthedocs.io/en/latest/
def look_at(
    camera_pos: np.ndarray,
    target: np.ndarray,
    up: np.ndarray = np.array([0.0, 1.0, 0.0], dtype=np.float32)
) -> np.ndarray:
    """Create a camera pose matrix."""
    camera_pos = np.asarray(camera_pos, dtype=np.float32)
    target = np.asarray(target, dtype=np.float32)
    up = np.asarray(up, dtype=np.float32)

    # Direction camera -> target
    forward = target - camera_pos
    forward = forward / np.linalg.norm(forward)

    # Right vector
    right = np.cross(forward, up)
    right = right / np.linalg.norm(right)

    # Correct up vector
    true_up = np.cross(right, forward)
    true_up = true_up / np.linalg.norm(true_up)

    # Build pose matrix
    pose = np.eye(4, dtype=np.float32)
    pose[:3, 0] = right
    pose[:3, 1] = true_up
    pose[:3, 2] = -forward
    pose[:3, 3] = camera_pos

    return pose


#https://trimesh.org/
def get_views(glb_path:Path) -> Array:

    glb_path = Path(glb_path)

    # Load mesh
    mesh = trimesh.load_mesh(glb_path)

    # Get bounds
    bounds = mesh.bounds

    # Create scene
    scene = pyrender.Scene(bg_color=[255, 255, 255, 0])

    # Add mesh
    scene.add(pyrender.Mesh.from_trimesh(mesh, smooth=False))

    # Compute center
    center = (bounds[0] + bounds[1]) / 2.0

    # Compute size
    extent = bounds[1] - bounds[0]

    # Distance of camera
    radius = float(np.max(extent)) * DEFAULT_RADIUS_SCALE

    # Camera
    camera = pyrender.PerspectiveCamera(yfov=DEFAULT_CAMERA_YFOV)

    # Light
    light = pyrender.DirectionalLight(
        color=np.ones(3, dtype=np.float32),
        intensity=DEFAULT_LIGHT_INTENSITY
    )

    # Renderer
    renderer = pyrender.OffscreenRenderer(*DEFAULT_IMAGE_SIZE)

    # Camera positions
    camera_positions = [
        ("left", center + np.array([0.0, 0.0, radius])),
        ("right",  center + np.array([0.0, 0.0, -radius])),
        ("front", center + np.array([radius, 0.0, 0.0])),
        ("back",  center + np.array([-radius, 0.0, 0.0])),
    ]

    result_array = []

    for name, camera_pos in camera_positions:
        # Compute pose
        pose = look_at(camera_pos, center)

        # Add camera and light
        cam_node = scene.add(camera, pose=pose)
        light_node = scene.add(light, pose=pose)

        # Render
        color, _ = renderer.render(scene)

        result_array.append(Image.fromarray(color))

        # Remove nodes
        scene.remove_node(cam_node)
        scene.remove_node(light_node)

    # Cleanup renderer
    renderer.delete()

    return result_array
