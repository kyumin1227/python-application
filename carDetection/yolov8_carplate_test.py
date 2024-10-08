import cv2
import pytesseract
import numpy as np
from ultralytics import YOLO

# YOLOv8 모델 로드 (번호판 탐지용)
model = YOLO('/Users/kyumin/python-application/carDetection/YOLOv8/yolov8-custom_number_plate_toy/weights/best.pt')  # 번호판 감지 모델 경로 설정

# Tesseract 경로 설정 (필요 시)
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'  # Tesseract 설치 경로

# OpenCV 영상 캡처 설정
cap = cv2.VideoCapture(0)  # 0번 카메라 (또는 동영상 파일 경로)

def detect_license_plate_and_read(frame):
    # YOLOv8을 사용하여 번호판 감지
    results = model(frame)
    
    for result in results:
        boxes = result.boxes
        for box in boxes:
            xyxy = box.xyxy[0].cpu().numpy().astype(int)
            conf = box.conf[0].cpu().numpy()
            cls = int(box.cls[0].cpu().numpy())

            # 신뢰도가 높으면 해당 영역 추출
            if conf > 0.5:  # 원하는 신뢰도 임계값 설정
                x1, y1, x2, y2 = xyxy
                plate_img = frame[y1:y2, x1:x2]  # 번호판 영역 자르기

                # 번호판 이미지를 전처리 (흑백 변환, 이진화 등)
                gray_plate = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)
                _, thresh_plate = cv2.threshold(gray_plate, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

                # 번호판 이미지에서 텍스트 읽기 (OCR)
                plate_text = pytesseract.image_to_string(thresh_plate, config='--psm 7')  # 번호판 인식용 설정

                plate_text_build = ""

                for c in plate_text:
                    if c in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"):
                        plate_text_build += c
                        

                print(f"Detected License Plate: {plate_text_build}")

                # 번호판 영역을 화면에 표시
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, plate_text_build.strip(), (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    detect_license_plate_and_read(frame)

    cv2.imshow('License Plate Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
