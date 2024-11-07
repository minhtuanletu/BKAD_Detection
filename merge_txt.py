import os

input_folder = 'runs/detect/predict13/labels'
with open('predict.txt', 'w') as f_out:
    for dir in os.listdir(input_folder):
        file_name = dir.split('.')[:-1]
        file_name = '.'.join(file_name)
        path = os.path.join(input_folder, dir)
        with open(path, 'r') as f_in:
            for line in f_in.readlines():
                new_line = f'{file_name}.jpg {line}'
                f_out.write(new_line)