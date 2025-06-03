import argparse
import os
import sys
import torch
from pathlib import Path
from collections import defaultdict

from models.yolo import Model
from utils.datasets import create_dataloader
from utils.general import check_img_size
from utils.torch_utils import select_device

def testModel(weights, dataloader, device, imgsz):
    model = Model(weights['cfg'], ch=3, nc=weights['nc'])
    checkpoint = torch.load(weights['path'], map_location=device)
    model.load_state_dict(checkpoint['model'].float().state_dict(), strict=False)
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
    parser.add_argument('--cfgs', nargs='+', required=True, help='List of model cfgs for each weight')
    parser.add_argument('--data', type=str, required=True, help='data.yaml path')
    parser.add_argument('--img-size', type=int, default=640, help='Inference image size')
    parser.add_argument('--batch-size', type=int, default=4)
    parser.add_argument('--device', default='', help='cuda device or cpu')
    parser.add_argument('--threshold', type=int, default=3, help='Minimum difference in object count to flag')
    args = parser.parse_args()

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
    for w, cfg in zip(args.weights, args.cfgs):
        checkpoint = torch.load(w, map_location=device)
        nc = checkpoint['model'].nc if hasattr(checkpoint['model'], 'nc') else data['nc']
        results = testModel({'path': w, 'cfg': cfg, 'nc': nc}, dataloader, device, imgsz)
        all_results.append(results)

    image_paths = list(all_results[0].keys())

    with open('deviations.txt', 'w') as f:
        f.write("All images and detected object counts:\n")
        for path in image_paths:
            counts = [results[path] for results in all_results]
            line = f"{path}: {counts}\n"
            print(line, end='')
            f.write(line)
