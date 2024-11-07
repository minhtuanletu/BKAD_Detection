import cv2
import numpy as np
import random
import os

def read_yolo_labels(label_path):
    """Read YOLO label file and return bounding boxes."""
    bboxes = []
    with open(label_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            # YOLO format: class_id, x_center, y_center, width, height (all relative)
            class_id = int(parts[0])
            x_center, y_center, width, height = map(float, parts[1:])
            bboxes.append((class_id, x_center, y_center, width, height))
    return bboxes

def rotate_point(cx, cy, angle, px, py):
    """Rotate a point around a given center (cx, cy) by an angle in degrees."""
    angle_rad = np.radians(angle)
    cos_a = np.cos(angle_rad)
    sin_a = np.sin(angle_rad)
    # Translate point back to origin:
    px -= cx
    py -= cy
    # Rotate point
    xnew = px * cos_a - py * sin_a
    ynew = px * sin_a + py * cos_a
    # Translate point back:
    px = xnew + cx
    py = ynew + cy
    return px, py

def crop_rotate_paste(image, bbox, angle):
    """Crop the object from the image using the bounding box, rotate around its centroid, and paste back."""
    h, w = image.shape[:2]
    class_id, x_center, y_center, box_width, box_height = bbox

    # Convert from relative to absolute coordinates
    x_center = int(x_center * w)
    y_center = int(y_center * h)
    box_width = int(box_width * w)
    box_height = int(box_height * h)

    # Calculate the top-left corner of the bounding box
    x1 = int(x_center - box_width / 2)
    y1 = int(y_center - box_height / 2)

    # Crop the object from the image
    cropped = image[y1:y1 + box_height, x1:x1 + box_width]

    # Rotate the cropped image
    if cropped.size == 0:
        return image, bbox

    # Get the rotation matrix for rotating around the center
    center = (box_width // 2, box_height // 2)
    rot_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_cropped = cv2.warpAffine(cropped, rot_matrix, (box_width, box_height), flags=cv2.INTER_LINEAR)

    # Create a mask of the rotated object
    gray = cv2.cvtColor(rotated_cropped, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

    # Determine new paste coordinates
    new_x1 = max(0, x_center - box_width // 2)
    new_y1 = max(0, y_center - box_height // 2)

    # Paste the rotated object back onto the original image using the mask
    roi = image[new_y1:new_y1 + box_height, new_x1:new_x1 + box_width]
    roi_bg = cv2.bitwise_and(roi, roi, mask=cv2.bitwise_not(mask))
    rotated_fg = cv2.bitwise_and(rotated_cropped, rotated_cropped, mask=mask)
    combined = cv2.add(roi_bg, rotated_fg)
    image[new_y1:new_y1 + box_height, new_x1:new_x1 + box_width] = combined

    # Calculate new bounding box coordinates
    # Get corners of the original box
    original_corners = [
        (x1, y1), (x1 + box_width, y1),
        (x1, y1 + box_height), (x1 + box_width, y1 + box_height)
    ]
    # Rotate corners around the center point
    rotated_corners = [rotate_point(x_center, y_center, angle, x, y) for x, y in original_corners]
    # Find the new bounding box from the rotated points
    new_x_coords = [pt[0] for pt in rotated_corners]
    new_y_coords = [pt[1] for pt in rotated_corners]
    new_x1, new_x2 = int(min(new_x_coords)), int(max(new_x_coords))
    new_y1, new_y2 = int(min(new_y_coords)), int(max(new_y_coords))

    # Convert back to YOLO format
    new_x_center = ((new_x1 + new_x2) / 2) / w
    new_y_center = ((new_y1 + new_y2) / 2) / h
    new_width = (new_x2 - new_x1) / w
    new_height = (new_y2 - new_y1) / h

    return image, (class_id, new_x_center, new_y_center, new_width, new_height)

def main(image_path, label_path, output_image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Read YOLO label file
    bboxes = read_yolo_labels(label_path)

    new_bboxes = []

    # Process each bounding box
    for idx, bbox in enumerate(bboxes):
        # Generate a random angle for rotation
        random_angle = random.randint(-15, 15)

        # Crop, rotate, and paste the object
        modified_image, new_bbox = crop_rotate_paste(image, bbox, random_angle)
        new_bboxes.append(new_bbox)

    # Save the final output image
    cv2.imwrite(output_image_path, modified_image)
    print(f"Saved modified image: {output_image_path}")

if __name__ == "__main__":
    for idx, dir in enumerate(os.listdir('data/train/images')):
        file_name = dir.split('.')[:-1]
        file_name = '.'.join(file_name)
        image_path = os.path.join('data/train/images', dir)
        label_path = os.path.join('data/train/labels', f'{file_name}.txt')
        output_image_path = os.path.join('synthetic/images', dir)
        main(image_path, label_path, output_image_path)
