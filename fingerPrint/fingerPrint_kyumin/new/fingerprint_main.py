import sys
import os
from PyQt5 import QtWidgets
from fingerprint_ui import FingerprintUI
from status_manager import set_mock_mode
from fingerprint_sensor import FingerprintSensor
from fingerprint_api import api_message, init_api
from queue import Queue

# 환경 변수 설정
USE_MOCK = len(sys.argv) > 1 and sys.argv[1] == "mock"
set_mock_mode(USE_MOCK)

def main():
	app = QtWidgets.QApplication(sys.argv)
	
	# UI 생성
	ui = FingerprintUI()
	
	# API 초기화
	init_api()
	
	# API 메시지 핸들러와 UI 연결
	api_message.message.connect(ui.set_success_message)
	
	# 센서 인스턴스 생성
	sensor = FingerprintSensor()
	sensor.fingerprint_detected.connect(ui.set_message)  # 센서 메시지도 UI에 표시
	sensor.error_occurred.connect(ui.set_message)  # 에러 메시지도 UI에 표시
	sensor.start()
	
	# UI 표시
	# ui.show()
	ui.showFullScreen()
	
	sys.exit(app.exec_())

if __name__ == "__main__":
	main()