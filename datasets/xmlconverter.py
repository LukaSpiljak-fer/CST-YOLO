import os
import xml.etree.ElementTree as ET

# Directory paths
xml_directory = "C:/Faks/CST-YOLO/Datasets/BCCD_Dataset-master/BCCD/Annotations"
output_directory = "C:/Faks/CST-YOLO/Datasets/BCCD_Dataset-master/BCCD/txtAnn"

# Class mapping (update as per your dataset)
class_mapping = {
    "RBC": 0,  # Example class mappings
    "WBC": 1,  # Add more classes as necessary
    "Platelet": 2
}

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Function to convert XML annotation to YOLO format
def convert_xml_to_txt(xml_file_path, output_txt_path):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    image_width = int(root.find(".//size/width").text)
    image_height = int(root.find(".//size/height").text)

    lines = []

    for obj in root.findall(".//object"):
        class_name = obj.find("name").text
        if class_name not in class_mapping:
            continue  # Skip unknown classes
        class_id = class_mapping[class_name]

        bndbox = obj.find(".//bndbox")
        xmin = int(bndbox.find("xmin").text)
        ymin = int(bndbox.find("ymin").text)
        xmax = int(bndbox.find("xmax").text)
        ymax = int(bndbox.find("ymax").text)

        # YOLO format calculations
        x_center = ((xmin + xmax) / 2) / image_width
        y_center = ((ymin + ymax) / 2) / image_height
        box_width = (xmax - xmin) / image_width
        box_height = (ymax - ymin) / image_height

        line = f"{class_id} {x_center} {y_center} {box_width} {box_height}"
        lines.append(line)

    # Write to txt file
    with open(output_txt_path, 'w') as txt_file:
        txt_file.write("\n".join(lines))

# Process each XML file in the directory
for xml_filename in os.listdir(xml_directory):
    if xml_filename.endswith(".xml"):
        xml_file_path = os.path.join(xml_directory, xml_filename)
        txt_filename = os.path.splitext(xml_filename)[0] + ".txt"
        output_txt_path = os.path.join(output_directory, txt_filename)
        convert_xml_to_txt(xml_file_path, output_txt_path)

print("Conversion complete. TXT annotations saved.")
