import json
# read metadata json

import argparse
# read command line arguments

from pathlib import Path
from typing import List
# handle file paths

import open_clip
# load CLIP model

import torch
# run model


from PIL import Image
# open images



#https://github.com/mlfoundations/open_clip

DEFAULT_VIEWS = ["front.png", "left.png", "right.png", "back.png"]



def load_model(device: str, model_name: str, pretrained: str):
    model, _, preprocess = open_clip.create_model_and_transforms(
        model_name,
        pretrained=pretrained,
    )
    # load model

    model.eval()
    # eval mode

    model = model.to(device)
    # move to device

    tokenizer = open_clip.get_tokenizer(model_name)
    # tokenizer

    return model, preprocess, tokenizer

#https://en.wikipedia.org/wiki/Cosine_similarity
#https://docs.pytorch.org/docs/stable/generated/torch.no_grad.html
def compute_similarity(model, preprocess, tokenizer, image: Image.Image, text: str, device: str) -> float:
    image = image.convert("RGB")
    # open image

    image = preprocess(image).unsqueeze(0).to(device)
    # preprocess

    tokens = tokenizer([text]).to(device)
    # tokenize

    with torch.no_grad():
        image_features = model.encode_image(image)
        # encode image

        image_features = image_features / image_features.norm(dim=-1, keepdim=True)
        # normalize

        text_features = model.encode_text(tokens)
        # encode text

        text_features = text_features / text_features.norm(dim=-1, keepdim=True)
        # normalize

        similarity = (image_features @ text_features.T).item()
        # similarity

    return float(similarity)


def evaluate_view(
    model,
    preprocess,
    tokenizer,
    image: Image.Image,
    prompt: str,
    device: str,
) -> dict:
    score = compute_similarity(model, preprocess, tokenizer, image, prompt, device)
    # compute score

    return {
        "full_prompt_score": float(score),
    }

def evaluate_folder(
    views:List[Image.Image],
    device: str,
    prompt: str = "",
    model_name: str = "ViT-B-32",
    pretrained: str = "laion2b_s34b_b79k",
) -> dict:

    model, preprocess, tokenizer = load_model(device, model_name, pretrained)
    # load model

    per_view_results = {}
    for i, view in enumerate(views):

        per_view_results[DEFAULT_VIEWS[i]] = evaluate_view(
            model=model,
            preprocess=preprocess,
            tokenizer=tokenizer,
            image=view,
            prompt=prompt,
            device=device,
        )

    scores = [v["full_prompt_score"] for v in per_view_results.values()]
    # collect scores

    return {
        "aggregate_scores": {
            # keep same names for compatibility
            "combined_mean": float(sum(scores) / len(scores)),
            "combined_min": float(min(scores)),
            "combined_max": float(max(scores)),
        },
        "num_views_evaluated": len(per_view_results),
    }
