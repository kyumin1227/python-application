import cv2
import torch
import numpy as np
from ultralytics import YOLO
import math

def detect_objects(video_source=0, model_path='/Users/kyumin/python-application/carDetection/YOLOv8/yolov8-parking_space7/weights/best.pt', img_size=640):
    # YOLOv8 모델 로드
    model = YOLO(model_path)

    # 웹캠 비디오 캡처 설정
    cap = cv2.VideoCapture(video_source)

    while True:

        zones = {
            "A1": 3,
            "A2": 3,
            "A3": 3
        }

        zone_coordinates = {
            "A1": (870, 800),
            "A2": (1160, 800),
            "A3": (1400, 800)
        }

        zone_list = ("A1", "A2", "A3")

        white = (255, 255, 255)
        black = (0, 0, 0)
        yellow = (255, 255, 0)
        red = (255, 0, 0)
        blue = (0, 0, 255)
        green = (0, 255, 0)

        colors = (blue, red, green, yellow)

        ret, frame = cap.read()
        if not ret:
            break

        # 객체 탐지
        results = model.predict(frame, imgsz=img_size)
        det = results[0].boxes.data.cpu().numpy()  # 검출된 결과를 NumPy 배열로 변환

        # 탐지 결과 처리
        if len(det):
            for box in det:
                x1, y1, x2, y2, conf, cls = box
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2

                if conf >= 0.6:
                    for zone in zone_list:
                        if is_point_in_circle((center_x, center_y), 100, zone_coordinates[zone]):
                            zones[zone] = int(cls)

                # if conf >= 0.5:
                #     label = f'{model.names[int(cls)]} {conf:.2f}'
                #     plot_one_box([x1, y1, x2, y2], frame, label=label, color=colors[int(cls)], line_thickness=2)

        # 구역 표시
        for zone in zone_list:
            cv2.circle(frame, zone_coordinates[zone], 30, colors[zones[zone]], -1)
        text = f"Total: {len(zone_list)}, Occupied: {tuple(zones.values()).count(0)}\
, Parking in progress: {tuple(zones.values()).count(1)}\
, Vacant: {tuple(zones.values()).count(2)}"
        # cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, text, (800, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow('YOLOv8 Zone Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
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

def is_point_in_circle(center, radius, point):
    # 원의 중심 좌표와 점의 좌표를 받아서 두 점 사이의 거리를 계산
    distance = math.sqrt((center[0] - point[0])**2 + (center[1] - point[1])**2)
    
    # 거리가 반지름보다 작거나 같으면 원과 겹침
    if distance <= radius:
        return True
    
    return False

if __name__ == '__main__':
    detect_objects()
