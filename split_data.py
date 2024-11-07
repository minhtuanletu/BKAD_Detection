import os
from PIL import Image

# images_output_path = 'data/train/images'
# labels_output_path = 'data/train/labels'
input_path = 'train_old_20241016'

# os.makedirs(images_output_path, exist_ok=True)
# os.makedirs(labels_output_path, exist_ok=True)
# idx = len(os.listdir(images_output_path))
for dir in os.listdir(input_path):
    folder = os.path.join(input_path, dir)
    images_output_path = f'data/{input_path}_{dir}/images'
    labels_output_path = f'data/{input_path}_{dir}/labels'
    os.makedirs(images_output_path, exist_ok=True)
    os.makedirs(labels_output_path, exist_ok=True)
    idx = len(os.listdir(images_output_path))
    for file in os.listdir(folder):
        if file.endswith(('.png', '.jpg')):
            file_name = file.split('.')[:-1]
            file_name = '.'.join(file_name)
            image_path = os.path.join(folder, file)
            label_path = os.path.join(folder, f'{file_name}.txt')
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