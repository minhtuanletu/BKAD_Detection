import os
from PIL import Image

images_output_path = 'dataset_new/images'
labels_output_path = 'dataset_new/labels'
input_path = 'data'

os.makedirs(images_output_path, exist_ok=True)
os.makedirs(labels_output_path, exist_ok=True)
idx = len(os.listdir(images_output_path))
# dirs = ['daytime', 'nighttime']
dirs = os.listdir(input_path)
for dir in dirs:
    folder = os.path.join(input_path, dir)
    images_folder = os.path.join(folder, 'images')
    for file in os.listdir(images_folder):
        file_name = file.split('.')[:-1]
        file_name = '.'.join(file_name)
        image_path = os.path.join(folder, 'images', file)
        label_path = os.path.join(folder, 'labels', f'{file_name}.txt')
        new_image_path = os.path.join(images_output_path, f'image{idx}.jpg')
        new_label_path = os.path.join(labels_output_path, f'image{idx}.txt')
        image = Image.open(image_path)
        image.save(new_image_path)
        with open(new_label_path, 'w') as f_out:
            with open(label_path, 'r') as f_in:
                for line in f_in.readlines():
                    line = line.rstrip().split(' ')
                    new_line = []
                    if line[0] == '4': line[0] = '0'
                    elif line[0] == '5': line[0] = '1'
                    elif line[0] == '6': line[0] = '2'
                    elif line[0] == '7': line[0] = '3'
                    new_line = ' '.join(line)
                    f_out.write(new_line + '\n')
        idx += 1