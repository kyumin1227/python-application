import sys
import os

# YOLOv5 디렉토리 경로 추가
yolov5_path = "/Users/kyumin/python-application/carDetection/yolov5"
if yolov5_path not in sys.path:
    sys.path.append(yolov5_path)

import cv2
import torch
from yolov5.models.common import DetectMultiBackend
from yolov5.utils.general import non_max_suppression, scale_boxes
from yolov5.utils.torch_utils import select_device
import numpy as np

def detect_objects(video_source=0, model_path='yolov5m.pt', img_size=640):
    # YOLO 모델 로드
    device = select_device('')
    model = DetectMultiBackend(model_path, device=device)
    names = model.names

    # 웹캠 비디오 캡처 설정
    cap = cv2.VideoCapture(video_source)

    # 구역 좌표
    zone_top_left = (100, 100)
    zone_bottom_right = (500, 500)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 이미지 전처리
        img = cv2.resize(frame, (img_size, img_size))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img / 255.0
        img = np.transpose(img, (2, 0, 1))
        img = np.expand_dims(img, axis=0)
        img = torch.from_numpy(img).float().to(device)

        # 객체 탐지
        pred = model(img)
        det = non_max_suppression(pred, conf_thres=0.25, iou_thres=0.45)[0]

        # 탐지 결과 처리
        if len(det):
            det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], frame.shape).round()
            for *xyxy, conf, cls in det:
                # print(xyxy, conf, cls)
                x1, y1, x2, y2 = map(int, xyxy)
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2

                # 구역 안에 들어온 경우
                if (zone_top_left[0] < center_x < zone_bottom_right[0]) and (zone_top_left[1] < center_y < zone_bottom_right[1]):
                    color = (0, 255, 0)
                    # print(f"{names[int(cls)]} {conf:.2f}")
                else:
                    color = (0, 0, 255)

                label = f'{names[int(cls)]} {conf:.2f}'
                if conf >= 0.5:
                    plot_one_box(xyxy, frame, label=label, color=color, line_thickness=2)

        cv2.rectangle(frame, zone_top_left, zone_bottom_right, (255, 255, 0), 2)
        cv2.imshow('YOLOv5 Zone Detection', frame)

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
