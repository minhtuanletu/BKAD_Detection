import cv2
import os
from PIL import Image

def draw_bbox(image, bbox):
    image = cv2.rectangle(image, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (255, 0, 0), 2)
    return image


def main():
    image_folder = f'data/val/images/'
    label_folder = f'data/val/labels/'
    output_folder = f'output/val/images'
    os.makedirs(output_folder, exist_ok=True)
    list_file = os.listdir(image_folder)
    for dir in list_file:
        file_name = dir.split('.')[:-1]
        file_name = '.'.join(file_name)
        image_path = os.path.join(image_folder, dir)
        label_path = os.path.join(label_folder, f'{file_name}.txt')
        if os.path.exists(label_path):
            image = cv2.imread(image_path)
            img_height, img_width = image.shape[:2]
            with open(label_path, 'r') as f:
                for line in f.readlines():
                        output = line.rstrip().split(' ')
                        if output[0] == '1':
                            x_center = int(float(output[1]) * img_width)
                            y_center = int(float(output[2]) * img_height)
                            w = int(float(output[3]) * img_width)
                            h = int(float(output[4]) * img_height)
                            x_min = int(x_center - w / 2)
                            y_min = int(y_center - h / 2)
                            x_max = int(x_center + w / 2)
                            y_max = int(y_center + h / 2)
                            bbox = [x_min, y_min, x_max, y_max]
                            image = draw_bbox(image, bbox)
            pil_image = Image.fromarray(image)
            new_path = os.path.join(output_folder, dir)
            pil_image.save(new_path)

main()