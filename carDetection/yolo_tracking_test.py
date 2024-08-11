import sys
import os
import cv2
import torch

# YOLOv5 디렉토리 경로 추가
yolov5_path = "/Users/kyumin/python-application/carDetection/yolov5"
if yolov5_path not in sys.path:
    sys.path.append(yolov5_path)

sys.path.append("/Users/kyumin/python-application/carDetection/sort")

from yolov5.models.common import DetectMultiBackend
from yolov5.utils.general import non_max_suppression, scale_boxes
from yolov5.utils.torch_utils import select_device
import numpy as np
from sort import Sort  # SORT 알고리즘을 사용하기 위해 필요한 모듈

def detect_and_track(video_source=0, model_path='yolov5m.pt', img_size=640):
    # YOLO 모델 로드
    device = select_device('')
    model = DetectMultiBackend(model_path, device=device)
    names = model.names

    # SORT 객체 추적기 초기화
    tracker = Sort()

    # 웹캠 비디오 캡처 설정
    cap = cv2.VideoCapture(video_source)

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

        # 탐지 결과 처리 및 추적
        if len(det):
            det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], frame.shape).round()

            # SORT 추적기 업데이트
            track_bbs_ids = tracker.update(det.cpu().numpy())

            for *xyxy, track_id in track_bbs_ids:
                x1, y1, x2, y2 = map(int, xyxy)
                label = f'ID {int(track_id)}'
                plot_one_box([x1, y1, x2, y2], frame, label=label, color=(255, 0, 0), line_thickness=2)

        cv2.imshow('YOLOv5 Object Tracking', frame)

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
    detect_and_track()
