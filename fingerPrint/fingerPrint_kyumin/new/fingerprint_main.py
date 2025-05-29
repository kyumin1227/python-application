import sys
import os
from PyQt5 import QtWidgets
from fingerprint_ui import FingerprintUI
from status_manager import set_mock_mode

# 환경 변수 설정
USE_MOCK = len(sys.argv) > 1 and sys.argv[1] == "mock"
set_mock_mode(USE_MOCK)

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = FingerprintUI()
	# window.showFullScreen()
	window.show()
	sys.exit(app.exec_())