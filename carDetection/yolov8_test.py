import cv2
import torch
import numpy as np
from ultralytics import YOLO

def detect_objects(video_source=0, model_path='yolov8m.pt', img_size=640):
    # YOLOv8 모델 로드
    model = YOLO(model_path)

    # 웹캠 비디오 캡처 설정
    cap = cv2.VideoCapture(video_source)

    # 구역 좌표
    zone_top_left = (100, 100)
    zone_bottom_right = (500, 500)

    while True:
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

                # 구역 안에 들어온 경우
                if (zone_top_left[0] < center_x < zone_bottom_right[0]) and (zone_top_left[1] < center_y < zone_bottom_right[1]):
                    color = (0, 255, 0)
                else:
                    color = (0, 0, 255)

                if conf >= 0.5:
                    label = f'{model.names[int(cls)]} {conf:.2f}'
                    plot_one_box([x1, y1, x2, y2], frame, label=label, color=color, line_thickness=2)

        # 구역 표시
        cv2.rectangle(frame, zone_top_left, zone_bottom_right, (255, 255, 0), 2)
        cv2.line(frame, (500, 0), (600, 1200), (255, 255, 0), 2)
        cv2.line(frame, (1000, 0), (1000, img_size), (255, 255, 0), 2)
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

if __name__ == '__main__':
    detect_objects()
