import sys
import os
from PyQt5 import QtWidgets
from fingerprint_ui import FingerprintUI
from status_manager import set_mock_mode
from fingerprint_sensor import FingerprintSensor
from queue import Queue

# 환경 변수 설정
USE_MOCK = len(sys.argv) > 1 and sys.argv[1] == "mock"
set_mock_mode(USE_MOCK)

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = FingerprintUI()
	
	# 지문 데이터 전달을 위한 큐 생성
	fingerprint_queue = Queue()
	
	# UI 먼저 표시
	# window.showFullScreen()
	window.show()
	
	# 센서 스레드 생성 및 시작
	sensor = FingerprintSensor(fingerprint_queue)
	sensor.start()
	
	sys.exit(app.exec_())