import os

a = []
for dir in os.listdir('data/train/labels'):
    path = os.path.join('data/train/labels/', dir)
    with open(path, 'r') as f:
        for line in f.readlines():
            line = line.rstrip().split(' ')
            a.append(line[0])
print(set(a))

a = []
for dir in os.listdir('data/val/labels'):
    path = os.path.join('data/val/labels/', dir)
    with open(path, 'r') as f:
        for line in f.readlines():
            line = line.rstrip().split(' ')
            a.append(line[0])
print(set(a))