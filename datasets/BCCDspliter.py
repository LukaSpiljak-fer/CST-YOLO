import os
import shutil

# Define paths
list_file_path = r'C:\Faks\cstyolo\CST-YOLO\datasets\BCCD_Dataset-master\scripts\val.txt'  # Path to the text file containing the list of filenames
source_folder = r'C:\Faks\cstyolo\CST-YOLO\datasets\BCCD_Dataset-master\BCCD\Annotations'       # Path to the folder containing the XML files
destination_folder = r'C:\Faks\cstyolo\CST-YOLO\datasets\BCCD_Dataset-master\BCCD\Annotations\val'     # Path to the new folder where files will be moved

# Create the destination folder if it doesn't exist
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# Read the list of filenames from the text file
with open(list_file_path, 'r') as file:
    filenames = file.read().splitlines()

# Move the corresponding XML files to the new folder
for filename in filenames:
    xml_filename = f"{filename}.xml"
    source_path = os.path.join(source_folder, xml_filename)
    destination_path = os.path.join(destination_folder, xml_filename)
    
    if os.path.exists(source_path):
        shutil.move(source_path, destination_path)
        print(f"Moved: {xml_filename}")
    else:
        print(f"File not found: {xml_filename}")

print("File moving completed.")