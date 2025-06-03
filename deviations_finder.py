import argparse
import os
import sys
import torch
from pathlib import Path
from collections import defaultdict

from models.experimental import attempt_load
from utils.datasets import create_dataloader
from utils.general import check_img_size
from utils.torch_utils import select_device

def testModel(weight_path, dataloader, device, imgsz):
    model = attempt_load(weight_path, map_location=device)
    model.to(device).eval()
    results = {}
    for imgs, _, paths, _ in dataloader:
        imgs = imgs.to(device).float() / 255.0
        with torch.no_grad():
            preds = model(imgs)
        for i, path in enumerate(paths):
            num_objs = (preds[i][:, 4] > 0.25).sum().item()
            results[path] = num_objs
    return results

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', required=True, help='List of weights/checkpoints to compare')
    parser.add_argument('--data', type=str, required=True, help='data.yaml path')
    parser.add_argument('--img-size', type=int, default=640, help='Inference image size')
    parser.add_argument('--batch-size', type=int, default=4)
    parser.add_argument('--device', default='', help='cuda device or cpu')
    parser.add_argument('--threshold', type=int, default=3, help='Minimum difference in object count to flag')
    args = parser.parse_args()
    args.single_cls = False

    # Load data.yaml
    import yaml
    with open(args.data) as f:
        data = yaml.safe_load(f)
    test_path = data['val']

    device = select_device(args.device)
    imgsz = check_img_size(args.img_size, 32)

    dataloader, dataset = create_dataloader(
        test_path, imgsz, args.batch_size, 32, args, hyp=None, augment=False, cache=False, rect=True, rank=-1,
        world_size=1, workers=2, pad=0.5, prefix='')

    all_results = []
    for w in args.weights:
        results = testModel(w, dataloader, device, imgsz)
        all_results.append(results)

    image_paths = list(all_results[0].keys())

    with open('deviations.txt', 'w') as f:
        f.write("All images and detected object counts:\n")
        for path in image_paths:
            counts = [results[path] for results in all_results]
            line = f"{path}: {counts}\n"
            print(line, end='')
            f.write(line)

    flagged = []
    for path in image_paths:
        counts = [results[path] for results in all_results]
        if max(counts) - min(counts) >= args.threshold:
            flagged.append((path, counts))
    with open('deviations.txt', 'a') as f:
        f.write("\nImages with strong deviations:\n")
        print("\nImages with strong deviations:")
        for path, counts in flagged:
            line = f"{path}: {counts}\n"
            print(line, end='')
            f.write(line)
