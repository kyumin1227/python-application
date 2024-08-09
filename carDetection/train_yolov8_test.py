from ultralytics import YOLO

# 모델 로드
model = YOLO('yolov8m.pt')  # YOLOv8 small 모델 사용, 필요에 따라 'yolov8m.pt', 'yolov8l.pt', 'yolov8x.pt' 등 사용

# 데이터셋 경로
data = './Detect_car.v3i.yolov5pytorch/data.yaml'  # dataset.yaml 파일의 경로

# 학습
model.train(data=data, epochs=50, imgsz=640, batch=16, name='yolov8-custom', project='YOLOv8')

# 추가적인 파라미터 설정 가능
# model.train(data=data, epochs=50, imgsz=640, batch=16, lr0=0.01, name='yolov8-custom', project='YOLOv8', device='cuda:0')
