import json
# read json output

import argparse
# read command line arguments

from pathlib import Path
from typing import List
# handle file paths

import torch
# run metric on cpu or gpu

import pyiqa
# load image quality metric

from PIL import Image
# open images


DEFAULT_VIEWS = ["front.png", "left.png", "right.png", "back.png"]
# default view names


def load_metric(metric_name: str, device: str):
    metric = pyiqa.create_metric(metric_name, device=device)
    # load pyiqa metric

    return metric


def compute_score(metric, image: Image.Image) -> float:
    with torch.no_grad():
        score = metric(image).item()
        # compute score

    return float(score)


def evaluate_view(
    metric,
    image: Image.Image,
) -> dict:
    score = compute_score(metric, image)
    # compute score

    return {
        "score": float(score),
    }


def evaluate_folder(
    views: List[Image.Image],
    device: str,
    metric_name: str = "nima",
) -> dict:
    metric = load_metric(metric_name, device)
    # load metric

    per_view_results = {}
    for i, view in enumerate(views):
        per_view_results[DEFAULT_VIEWS[i]] = evaluate_view(
            metric=metric,
            image=view,
        )

    scores = [v["score"] for v in per_view_results.values()]
    # collect scores

    return {
        "aggregate_scores": {
            "mean": float(sum(scores) / len(scores)),
            "min": float(min(scores)),
            "max": float(max(scores)),
        },
        "num_views_evaluated": len(per_view_results),
    }


def main():
    parser = argparse.ArgumentParser(description="Compute NIMA scores for one generation folder.")
    # create parser

    parser.add_argument(
        "--folder",
        type=str,
        required=True,
        help="Folder containing rendered view PNGs",
    )
    parser.add_argument(
        "--output_json",
        type=str,
        default=None,
        help="Optional output JSON path",
    )
    parser.add_argument(
        "--metric_name",
        type=str,
        default="nima",
        help="PyIQA metric name to use",
    )
    parser.add_argument(
        "--device",
        type=str,
        default=None,
        help="cuda or cpu",
    )

    args = parser.parse_args()
    # parse args

    folder = Path(args.folder)
    # input folder

    device = args.device or ("cuda" if torch.cuda.is_available() else "cpu")
    # choose device

    views = [Image.open(folder / view) for view in DEFAULT_VIEWS if (folder / view).exists()]
    # load images

    results = evaluate_folder(
        views=views,
        device=device,
        metric_name=args.metric_name,
    )
    # compute results

    output_json = Path(args.output_json) if args.output_json else folder / "nima_eval.json"
    # choose output path

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
        # save json

    print(f"Saved evaluation to: {output_json}")


if __name__ == "__main__":
    main()
