import os

def remap_classes_in_yolo_labels(folder_path):
    class_map = {0: 2, 1: 1, 2: 0}
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                new_lines = []
                for line in lines:
                    parts = line.strip().split()
                    if not parts:
                        continue
                    try:
                        old_class = int(parts[0])
                        new_class = class_map.get(old_class, old_class)
                        parts[0] = str(new_class)
                        new_lines.append(' '.join(parts) + '\n')
                    except Exception:
                        new_lines.append(line)
                with open(file_path, 'w') as f:
                    f.writelines(new_lines)

if __name__ == "__main__":
    labels_folder = r"c:\faks\CST-YOLO\CST-YOLO\datasets\bcd\test\labels"
    remap_classes_in_yolo_labels(labels_folder)
