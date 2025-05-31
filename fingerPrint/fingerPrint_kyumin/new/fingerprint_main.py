import sys
from PyQt5 import QtWidgets
from fingerprint_ui import FingerprintUI
from status_manager import set_mock_mode
from fingerprint_sensor import FingerprintSensor
from fingerprint_api import api_message, init_api

# 모드 설정
USE_MOCK = len(sys.argv) > 1 and sys.argv[1] == "mock"
set_mock_mode(USE_MOCK)

def main():
	app = QtWidgets.QApplication(sys.argv)
	
	# UI 생성
	ui = FingerprintUI()
	
	# API 초기화
	init_api()
	
	# API 메시지 핸들러와 UI 연결
	api_message.message.connect(ui.set_info_message)
	
	# 센서 인스턴스 생성
	sensor = FingerprintSensor()
	sensor.message.connect(ui.set_info_message)
	sensor.start()
	
	# UI 표시
	ui.showFullScreen()
	
	sys.exit(app.exec_())

if __name__ == "__main__":
	main()