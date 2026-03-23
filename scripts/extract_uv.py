import argparse
import trimesh
import sys
from PIL import Image

def extract_uv_texture(glb_path, output_png_path):
    try:
        scene = trimesh.load(glb_path, force='scene')
        
        texture_found = False

        for name, geometry in scene.geometry.items():
            if hasattr(geometry, 'visual') and hasattr(geometry.visual, 'material'):
                material = geometry.visual.material
                
                if hasattr(material, 'image') and material.image is not None:
                    image = material.image
                    texture_found = True
                elif hasattr(material, 'baseColorTexture') and material.baseColorTexture is not None:
                    image = material.baseColorTexture
                    texture_found = True
                    
                if texture_found:
                    image.save(output_png_path)
                    return
        
        if not texture_found:
            print("No texture found in this GLB file.")
            
    except Exception as e:
        print(f"Error while extracting : {e}")
