import os
from glob import glob

DETECT_DIR = os.path.join('runs', 'detect')
OUTPUT_FILE = 'deviations.txt'

model_dirs = [d for d in os.listdir(DETECT_DIR) if os.path.isdir(os.path.join(DETECT_DIR, d))]
model_dirs.sort()

first_labels_dir = os.path.join(DETECT_DIR, model_dirs[0], 'labels')
label_files = [os.path.basename(f) for f in glob(os.path.join(first_labels_dir, '*.txt'))]
label_files.sort()

results = {}
for label_file in label_files:
    counts = []
    for model in model_dirs:
        label_path = os.path.join(DETECT_DIR, model, 'labels', label_file)
        if os.path.exists(label_path):
            with open(label_path, 'r') as f:
                lines = f.readlines()
            counts.append(len(lines))
        else:
            counts.append(0)
    results[label_file] = counts

with open(OUTPUT_FILE, 'w') as out:
    out.write('# ' + ' '.join(model_dirs) + '\n')
    for label_file, counts in results.items():
        out.write(f'{label_file} {counts}\n')

print(f'Results written to {OUTPUT_FILE}')