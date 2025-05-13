import cv2

def drawABox(image_path, annotation_path, output_path):
    image = cv2.imread(image_path)
    img_height, img_width = image.shape[:2]

    with open(annotation_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        class_id, x_center, y_center, width, height = map(float, line.strip().split())

        x_center *= img_width
        y_center *= img_height
        width *= img_width
        height *= img_height

        x1 = int(x_center - width / 2)
        y1 = int(y_center - height / 2)
        x2 = int(x_center + width / 2)
        y2 = int(y_center + height / 2)

        cv2.rectangle(image, (x1, y1), (x2, y2), color=(0, 255, 0), thickness=2)
        cv2.putText(image, f'Class {int(class_id)}', (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    cv2.imwrite(output_path, image)
    print(f"Output saved to {output_path}")

drawABox('test/BloodImage_00007.jpg', 'txtAnn/test/BloodImage_00007.txt', 'output.jpg')
