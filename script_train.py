from ultralytics import YOLO

model = YOLO('yolo11s.pt')

if __name__ == '__main__':
    results = model.train(data="data.yaml", epochs=100, batch=32, patience=10, project='training_result_new_31_10')
