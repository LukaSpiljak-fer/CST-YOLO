import os
import xml.etree.ElementTree as ET

def convert_annotation(xml_file, output_dir, class_mapping):
    """
    Converts a single XML annotation file to YOLO format.

    Args:
        xml_file (str): Path to the XML file.
        output_dir (str): Directory to save the YOLO format .txt file.
        class_mapping (dict): Mapping of class names to class IDs.
    """
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Get image dimensions
    size = root.find("size")
    width = int(size.find("width").text)
    height = int(size.find("height").text)

    # Prepare YOLO annotation content
    yolo_annotations = []

    for obj in root.findall("object"):
        # Get class name and map it to class ID
        class_name = obj.find("name").text
        if class_name not in class_mapping:
            raise ValueError(f"Class '{class_name}' not found in class_mapping.")
        class_id = class_mapping[class_name]

        # Get bounding box coordinates
        bndbox = obj.find("bndbox")
        xmin = int(bndbox.find("xmin").text)
        ymin = int(bndbox.find("ymin").text)
        xmax = int(bndbox.find("xmax").text)
        ymax = int(bndbox.find("ymax").text)

        # Convert to YOLO format (normalized x_center, y_center, width, height)
        x_center = (xmin + xmax) / 2 / width
        y_center = (ymin + ymax) / 2 / height
        box_width = (xmax - xmin) / width
        box_height = (ymax - ymin) / height

        # Append to YOLO annotations
        yolo_annotations.append(f"{class_id} {x_center} {y_center} {box_width} {box_height}")

    # Write YOLO annotations to a .txt file
    if yolo_annotations:
        output_file = os.path.join(output_dir, os.path.splitext(os.path.basename(xml_file))[0] + ".txt")
        with open(output_file, "w") as f:
            f.write("\n".join(yolo_annotations))

def convert_dataset(xml_dir, output_dir, class_mapping):
    """
    Converts all XML annotation files in a directory to YOLO format.

    Args:
        xml_dir (str): Directory containing XML annotation files.
        output_dir (str): Directory to save YOLO format .txt files.
        class_mapping (dict): Mapping of class names to class IDs.
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Process each XML file
    for xml_file in os.listdir(xml_dir):
        if xml_file.endswith(".xml"):
            xml_path = os.path.join(xml_dir, xml_file)
            convert_annotation(xml_path, output_dir, class_mapping)

    print(f"Conversion complete. YOLO annotations saved in '{output_dir}'.")

# Example usage
if __name__ == "__main__":
    # Define paths
    xml_dir = "path/to/xml/annotations"  # Directory containing XML files
    output_dir = "path/to/yolo/annotations"  # Directory to save YOLO format files

    # Define class mapping (class name -> class ID)
    class_mapping = {
        "WBC": 0,
        "RBC": 1,
        # Add more classes as needed
    }

    # Convert the dataset
    convert_dataset(xml_dir, output_dir, class_mapping)