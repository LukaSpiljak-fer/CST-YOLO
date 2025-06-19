import argparse
import os
import subprocess
from pathlib import Path
import yaml

def run_detect(weight, image_path, img_size, conf_thres, iou_thres, device, save_dir):
    # Use a unique subdirectory for each weight
    try:
        weight_name = weight.split('/')[3]
    except:
        try:
            wpath = weight.split('/')
            weight_name = wpath[len(wpath)-2]
        except:
            weight_name = "WrongName"
    exp_name = f'deviations_{weight_name}'
    label_dir = Path(save_dir) / exp_name / 'labels'
    label_dir.mkdir(parents=True, exist_ok=True)
    label_file = label_dir / (Path(image_path).stem + '.txt')
    if label_file.exists():
        label_file.unlink()
    # Run detect.py
    cmd = [
        'python', 'detect.py',
        '--weights', str(weight),
        '--source', str(image_path),
        '--img-size', str(img_size),
        '--conf-thres', str(conf_thres),
        '--iou-thres', str(iou_thres),
        '--device', str(device),
        '--save-txt',
        '--project', str(save_dir),
        '--name', exp_name,
        '--exist-ok'
    ]
    subprocess.run(cmd, check=True)
    # Count detections in label file
    if label_file.exists():
        with open(label_file, 'r') as f:
            count = sum(1 for _ in f)
    else:
        count = 0
    return count

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', required=True, help='List of weights/checkpoints to compare')
    parser.add_argument('--data', type=str, required=True, help='data.yaml path')
    parser.add_argument('--img-size', type=int, default=640, help='Inference image size')
    parser.add_argument('--conf-thres', type=float, default=0.25, help='object confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.65, help='IOU threshold for NMS')
    parser.add_argument('--device', default='0', help='cuda device or cpu')
    parser.add_argument('--output', type=str, default='deviations.txt', help='Output file')
    parser.add_argument('--conf-thres-list', nargs='+', type=float, help='List of confidence thresholds for each weight')
    parser.add_argument('--labels-dir', type=str, required=True, help='Directory containing ground truth label .txt files')
    args = parser.parse_args()

    # Load data.yaml
    with open(args.data) as f:
        data = yaml.safe_load(f)
    test_path = data['val']

    # Get all image paths
    if os.path.isdir(test_path):
        image_paths = [str(Path(test_path) / x) for x in os.listdir(test_path) if x.lower().endswith(('.jpg', '.jpeg', '.png'))]
    else:
        with open(test_path) as f:
            image_paths = [line.strip() for line in f if line.strip()]

    # Validate conf-thres-list
    if args.conf_thres_list:
        if len(args.conf_thres_list) != len(args.weights):
            raise ValueError('Length of --conf-thres-list must match number of --weights')

    results_per_image = {}
    for image_path in image_paths:
        counts = []
        for idx, weight in enumerate(args.weights):
            conf_thres = args.conf_thres_list[idx] if args.conf_thres_list else args.conf_thres
            count = run_detect(weight, image_path, args.img_size, conf_thres, args.iou_thres, args.device, 'runs/detect')
            counts.append(count)
        # Add ground truth count from label file
        label_file = Path(args.labels_dir) / (Path(image_path).stem + '.txt')
        if label_file.exists():
            with open(label_file, 'r') as lf:
                gt_count = sum(1 for _ in lf)
        else:
            gt_count = 0
        counts.append(gt_count)
        results_per_image[image_path] = counts

    with open(args.output, 'w') as f:
        f.write("All images and detected object counts (last value is ground truth):\n")
        for path, counts in results_per_image.items():
            line = f"{path}: {counts}\n"
            print(line, end='')
            f.write(line)