import torch
import cv2
import numpy as np
from ultralytics import YOLO

def detect_objects(image_path, model_path='yolov8m.pt', imgsz=640):
    # YOLOv8 모델 로드
    model = YOLO(model_path)

    # 이미지 로드
    img = cv2.imread(image_path)
    assert img is not None, f"Image Not Found {image_path}"

    # 이미지 전처리 및 객체 탐지
    results = model(img, imgsz=imgsz)

    # 결과 처리 및 네모 박스 그리기
    for result in results:
        boxes = result.boxes  # 바운딩 박스 정보
        for box in boxes:
            xyxy = box.xyxy[0].cpu().numpy().astype(int)
            conf = box.conf[0].cpu().numpy()
            cls = int(box.cls[0].cpu().numpy())
            label = f'{model.names[cls]} {conf:.2f}'
            plot_one_box(xyxy, img, label=label, color=(255, 0, 0), line_thickness=2)

    # 결과 이미지 보여주기
    cv2.imshow('YOLOv8 Detection', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def plot_one_box(xyxy, img, label=None, color=(255, 0, 0), line_thickness=3):
    c1, c2 = (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3]))
    cv2.rectangle(img, c1, c2, color, thickness=line_thickness, lineType=cv2.LINE_AA)
    if label:
        font_scale = 0.5
        font_thickness = max(line_thickness - 1, 1)
        t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)[0]
        c2 = (c1[0] + t_size[0], c1[1] - t_size[1] - 3)
        cv2.rectangle(img, c1, c2, color, -1, cv2.LINE_AA)
        cv2.putText(img, label, (c1[0], c1[1] - 2), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), font_thickness, cv2.LINE_AA)

if __name__ == '__main__':
    # 이미지 경로 및 모델 경로 설정
    image_path = '/Users/kyumin/python-application/carDetection/test/car_plate/image/15.jpg'
    model_path = '/Users/kyumin/python-application/carDetection/YOLOv8/yolov8-custom_car_plate3/weights/best.pt'  # or 'path/to/your/custom/model.pt'
    
    # 객체 탐지 및 네모 박스 그리기
    detect_objects(image_path, model_path)
