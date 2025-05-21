import os
import shutil

# Mapping dataset names and their specific subfolder names to unified names
datasets = {
    'cbc': {'Testing': 'test', 'Validation': 'valid', 'Training': 'train'},
    'bccd': {'testdata': 'test', 'validata': 'valid', 'traindata': 'train'},
    'bcd': {'test': 'test', 'valid': 'valid', 'train': 'train'}
}

# Create destination folder structure
for split in ['test', 'train', 'valid']:
    os.makedirs(f'all/{split}/images', exist_ok=True)
    os.makedirs(f'all/{split}/labels', exist_ok=True)

# Go through each dataset and move files
for dataset, subfolders in datasets.items():
    for src_subfolder, target_split in subfolders.items():
        src_images_path = os.path.join(dataset, src_subfolder, 'images')
        src_labels_path = os.path.join(dataset, src_subfolder, 'labels')

        if os.path.exists(src_images_path):
            for fname in os.listdir(src_images_path):
                if fname.lower().endswith('.jpg'):
                    new_fname = fname.replace('.jpg', f'{dataset}.jpg')
                    src = os.path.join(src_images_path, fname)
                    dst = os.path.join('all', target_split, 'images', new_fname)
                    shutil.copy2(src, dst)

        if os.path.exists(src_labels_path):
            for fname in os.listdir(src_labels_path):
                if fname.lower().endswith('.txt'):
                    new_fname = fname.replace('.txt', f'{dataset}.txt')
                    src = os.path.join(src_labels_path, fname)
                    dst = os.path.join('all', target_split, 'labels', new_fname)
                    shutil.copy2(src, dst)
