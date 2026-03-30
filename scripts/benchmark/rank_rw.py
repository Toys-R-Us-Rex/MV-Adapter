#!/usr/bin/env python3
import argparse
# read command line arguments

import json
# read and write json files

import shutil
# copy folders


from pathlib import Path
# handle file paths


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        # open json file
        return json.load(f)
        # parse json


def compute_scores(gen_dir: Path,nima_json_name,openclip_json_name) -> dict:
    openclip_path = gen_dir / openclip_json_name
    # openclip result file

    nima_path = gen_dir / nima_json_name
    # nima result file

    if not openclip_path.is_file():
        raise FileNotFoundError(f"Missing file: {openclip_path}")

    if not nima_path.is_file():
        raise FileNotFoundError(f"Missing file: {nima_path}")

    openclip_data = load_json(openclip_path)
    # load openclip json

    nima_data = load_json(nima_path)
    # load nima json

    clip_scores = openclip_data["aggregate_scores"]
    # openclip aggregate scores

    nima_scores = nima_data["aggregate_scores"]
    # nima aggregate scores

    clip_mean = float(clip_scores["combined_mean"])
    # average clip score

    clip_min = float(clip_scores["combined_min"])
    # lowest clip score

    nima_mean = float(nima_scores["mean"])
    # average nima score

    nima_min = float(nima_scores["min"])
    # lowest nima score

    clip_mean_norm = (clip_mean + 1.0) / 2.0
    # normalize clip mean from [-1, 1] to [0, 1]

    clip_min_norm = (clip_min + 1.0) / 2.0
    # normalize clip min from [-1, 1] to [0, 1]

    nima_mean_norm = nima_mean / 10.0
    # normalize nima mean from [0, 10] to [0, 1]

    nima_min_norm = nima_min / 10.0
    # normalize nima min from [0, 10] to [0, 1]

    prompt_subscore = 0.8 * clip_mean_norm + 0.2 * clip_min_norm
    # prompt score from clip

    aesthetic_subscore = 0.8 * nima_mean_norm + 0.2 * nima_min_norm
    # aesthetic score from nima

    final_score = 0.7 * prompt_subscore + 0.3 * aesthetic_subscore
    # final weighted score

    return {
        "generation": gen_dir.name,
        "path": str(gen_dir.resolve()),
        "openclip": {
            "combined_mean": clip_mean,
            "combined_min": clip_min,
            "combined_mean_normalized": clip_mean_norm,
            "combined_min_normalized": clip_min_norm,
        },
        "nima": {
            "mean": nima_mean,
            "min": nima_min,
            "mean_normalized": nima_mean_norm,
            "min_normalized": nima_min_norm,
        },
        "subscores": {
            "prompt_subscore": prompt_subscore,
            "aesthetic_subscore": aesthetic_subscore,
        },
        "final_score": final_score,
    }


def list_generation_dirs(run_dir: Path) -> list[Path]:
    gen_dirs = []
    # collect generation folders

    for p in run_dir.iterdir():
        # loop over items in run folder
        if p.is_dir() and p.name.startswith("gen_"):
            gen_dirs.append(p)
            # keep only gen_* folders

    return sorted(gen_dirs, key=lambda x: x.name)
    # sort by folder name


def copy_best_generations(top_entries: list[dict], best_dir: Path) -> None:
    if best_dir.exists():
        shutil.rmtree(best_dir)
        # remove old best folder

    best_dir.mkdir(parents=True, exist_ok=True)
    # create fresh best folder

    for rank, entry in enumerate(top_entries, start=1):
        src = Path(entry["path"])
        # source generation folder

        dst = best_dir / f"rank_{rank}_{src.name}"
        # destination folder

        shutil.copytree(src, dst)
        # copy full folder


def rank_generations(run_dir: str, top_k: int = 3, nima_json_name: str = "nima.json", openclip_json_name: str = "openclip.json") -> dict:
    run_dir = Path(run_dir).resolve()
    
    if not run_dir.is_dir():
        raise NotADirectoryError(f"Run directory does not exist: {run_dir}")
    
    gen_dirs = list_generation_dirs(run_dir)
    if not gen_dirs:
        raise RuntimeError(f"No gen_* folders found in: {run_dir}")
    
    ranking = [compute_scores(gen_dir, nima_json_name, openclip_json_name) for gen_dir in gen_dirs]
    ranking.sort(key=lambda x: x["final_score"], reverse=True)
    
    for idx, entry in enumerate(ranking, start=1):
        entry["rank"] = idx
    
    top_k = min(top_k, len(ranking))
    top_entries = ranking[:top_k]
    
    ranking_payload = {
        "run_dir": str(run_dir),
        "num_generations": len(ranking),
        "ranking_formula": {
            "prompt_weight": 0.7,
            "aesthetic_weight": 0.3,
            "prompt_subscore_formula": "0.8 * clip_mean_norm + 0.2 * clip_min_norm",
            "aesthetic_subscore_formula": "0.8 * nima_mean_norm + 0.2 * nima_min_norm",
            "clip_normalization": "(x + 1) / 2",
            "nima_normalization": "x / 10",
        },
        "ranked_generations": ranking,
    }
    
    with (run_dir / "ranking.json").open("w", encoding="utf-8") as f:
        json.dump(ranking_payload, f, indent=2)
    
    with (run_dir / f"top_{top_k}.json").open("w", encoding="utf-8") as f:
        json.dump({"run_dir": str(run_dir), "top_k": top_k, "top_generations": top_entries}, f, indent=2)
    
    copy_best_generations(top_entries, run_dir / "best")
    
    return ranking_payload
