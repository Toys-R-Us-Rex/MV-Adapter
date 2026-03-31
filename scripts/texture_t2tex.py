import argparse
import os
import sys
import random
import torch
import datetime
from mvadapter.pipelines.pipeline_texture import ModProcessConfig, TexturePipeline
from mvadapter.utils import make_image_grid
from .extract_uv import extract_uv_texture
import json
from PIL import PngImagePlugin
from pygltflib import GLTF2
from pathlib import Path
import shutil
from .benchmark.render_rw import get_views
from .benchmark.openclip_rw import evaluate_folder as evaluate_folder_openclip
from .benchmark.nima_rw import evaluate_folder as evaluate_folder_nima
from .benchmark.rank_rw import rank_generations
import json



OPENCLIP_FILENAME = "openclip_data.json"
NIMA_FILENAME = "nima_data.json"
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", type=str, default="cuda")
    parser.add_argument("--variant", type=str, default="sdxl", choices=["sdxl", "sd21"])
    # I/O
    parser.add_argument("--mesh", type=str, required=True)
    parser.add_argument("--text", type=str, required=True)
    parser.add_argument("--seed", type=int, default=-1)
    parser.add_argument("--save_dir", type=str, default="./output")
    parser.add_argument("--save_name", type=str, default="t2tex_sample")
    parser.add_argument("--guidance_scale", type=float, default=7.0)
    parser.add_argument("--num_inference_steps", type=int, default=50)
    parser.add_argument("--negative_text", type=str, default="watermark, ugly, deformed, noisy, blurry, low contrast")
    parser.add_argument("--num_generations", type=int, default=1)
    parser.add_argument("--benchmark_activated", type=str, default="False")
    
    # Extra
    parser.add_argument("--preprocess_mesh", action="store_true")
    args = parser.parse_args()

    if args.variant == "sdxl":
        from .inference_tg2mv_sdxl import prepare_pipeline, run_pipeline

        base_model = "Lykon/dreamshaper-xl-1-0"
        vae_model = "madebyollin/sdxl-vae-fp16-fix"
        height = width = 768
        uv_size = 1024
    elif args.variant == "sd21":
        from .inference_tg2mv_sd import prepare_pipeline, run_pipeline

        base_model = "Manojb/stable-diffusion-2-1-base"
        vae_model = None
        height = width = 512
        uv_size = 4096
    else:
        raise ValueError(f"Invalid variant: {args.variant}")

    device = args.device
    num_views = 6

    # Prepare pipelines
    pipe = prepare_pipeline(
        base_model=base_model,
        vae_model=vae_model,
        unet_model=None,
        lora_model=None,
        adapter_path="huanngzh/mv-adapter",
        scheduler=None,
        num_views=num_views,
        device=device,
        dtype=torch.float16,
    )
    texture_pipe = TexturePipeline(
        upscaler_ckpt_path="./checkpoints/RealESRGAN_x2plus.pth",
        inpaint_ckpt_path="./checkpoints/big-lama.pt",
        device=device,
    )
    print("Pipeline ready.")

    os.makedirs(args.save_dir, exist_ok=True)
    
    base_folder_path = Path(args.save_dir)
    
    for i in range(args.num_generations):
        gen_folder_path = base_folder_path / str(i)
        seed = random.randint(0, 2147483647) if args.seed == -1 else args.seed
        gen_folder_path.mkdir(parents=True, exist_ok=True)
    
        images, pos_images, normal_images = run_pipeline(
            pipe,
            mesh_path=args.mesh,
            num_views=num_views,
            text=args.text,
            height=height,
            width=width,
            num_inference_steps=args.num_inference_steps,
            guidance_scale=args.guidance_scale,
            seed=seed,
            negative_prompt=args.negative_text,
            device=device,
        )
        mv_path = gen_folder_path / f"{args.save_name}.png"
        
        metadata_dict = {
            "prompt": args.text,
            "negative_prompt": args.negative_text,
            "seed": seed,
            "steps": args.num_inference_steps,
            "guidance": args.guidance_scale,
            "base_model": base_model,
            "height": height,
            "width": width,
            "vae_model": vae_model,
            "uv_size": uv_size,
            "num_views": num_views,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        metadata_png = PngImagePlugin.PngInfo()
        metadata_png.add_text("parameters", json.dumps(metadata_dict))
        
        make_image_grid(images, rows=1).save(mv_path, pnginfo=metadata_png)
        json_path = gen_folder_path / f"{args.save_name}_meta.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(metadata_dict, f, indent=4)

        torch.cuda.empty_cache()

        out = texture_pipe(
            mesh_path=args.mesh,
            save_dir=args.save_dir,
            save_name=args.save_name,
            uv_unwarp=False,
            preprocess_mesh=False,
            uv_size=uv_size,
            rgb_path=mv_path,
            rgb_process_config=ModProcessConfig(view_upscale=True, inpaint_mode="view"),
            debug_mode=False
        )
        
        uv_png_path = gen_folder_path / "texture.png"
        
        extract_uv_texture(str(out.shaded_model_save_path), str(uv_png_path))
        
        model_output_path = gen_folder_path / f"texture.glb"
        shutil.copy(out.shaded_model_save_path,model_output_path)
        
        if args.benchmark_activated == "True":
            views = get_views(model_output_path)
            folder_data = evaluate_folder_openclip(
                views=views,
                device=device,
                prompt=args.text,
            )
            
            openclip_json_path = gen_folder_path / OPENCLIP_FILENAME
            with open(openclip_json_path, "w", encoding="utf-8") as f:
                json.dump(folder_data, f, indent=4)
            
            
            folder_data = evaluate_folder_nima(
                views=views,
                device=device
            )
            nima_json_path = gen_folder_path / NIMA_FILENAME
            with open(nima_json_path, "w", encoding="utf-8") as f:
                json.dump(folder_data, f, indent=4)
       
       
    if args.benchmark_activated == "True":         
        print("All generations completed. Starting ranking...")
        rank_generations(run_dir=base_folder_path, top_k=3, nima_json_name=NIMA_FILENAME, openclip_json_name=OPENCLIP_FILENAME)
        print("Benchmarking completed. - ranking saved in ranking.json")            
    print(f"Output saved to {uv_png_path}")
        
