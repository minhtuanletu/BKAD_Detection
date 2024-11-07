import random
import os
import shutil

images = os.listdir('dataset_new/images')
random.shuffle(images)
train_nums = int(len(images) * 1.0)

train_images = images[:train_nums]
val_images = images[train_nums:]

train_images_folder = 'training_data_new/train/images'
train_labels_folder = 'training_data_new/train/labels'
val_images_folder = 'training_data_new/val/images'
val_labels_folder = 'training_data_new/val/labels'
os.makedirs(train_images_folder, exist_ok=True)
os.makedirs(train_labels_folder, exist_ok=True)
os.makedirs(val_images_folder, exist_ok=True)
os.makedirs(val_labels_folder, exist_ok=True)
for image in train_images:
    file_name = image.split('.')[:-1]
    file_name = '.'.join(file_name)
    image_path = os.path.join('dataset_new/images', image)
    label_path = os.path.join('dataset_new/labels', f'{file_name}.txt')
    shutil.copy(image_path, train_images_folder)
    shutil.copy(label_path, train_labels_folder)

for image in val_images:
    file_name = image.split('.')[:-1]
    file_name = '.'.join(file_name)
    image_path = os.path.join('dataset/images', image)
    label_path = os.path.join('dataset/labels', f'{file_name}.txt')
    shutil.copy(image_path, val_images_folder)
    shutil.copy(label_path, val_labels_folder)