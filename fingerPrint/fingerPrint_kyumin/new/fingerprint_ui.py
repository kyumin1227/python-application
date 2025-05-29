from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTime, QDateTime, Qt
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from status_manager import Status, get_status, set_status
from threading import Timer

class FingerprintUI(QMainWindow):
	def __init__(self):
		super().__init__()
		# UI 파일 로드
		loadUi("new.ui", self)
		
		# 변수 초기화
		self.stdNum = ""
		
		# 페이지 버튼 연결
		self.fingerprint_button.clicked.connect(lambda: self.changePage(0))
		self.outing_button.clicked.connect(lambda: self.changePage(1))
		self.new_fingerprint_button.clicked.connect(lambda: self.changePage(2))
		
		# 버튼 이벤트 연결
		digit_buttons = {
			self.new_pushButton_0: "0",
			self.new_pushButton_1: "1",
			self.new_pushButton_2: "2",
			self.new_pushButton_3: "3",
			self.new_pushButton_4: "4",
			self.new_pushButton_5: "5",
			self.new_pushButton_6: "6",
			self.new_pushButton_7: "7",
			self.new_pushButton_8: "8",
			self.new_pushButton_9: "9",
		}
		
		# 숫자 버튼 이벤트 연결
		for button, digit in digit_buttons.items():
			button.clicked.connect(lambda _, d=digit: self.changeStdNum(d))
		
		# 기타 버튼 이벤트 연결
		self.new_pushButton_back.clicked.connect(lambda: self.changeStdNum("back"))
		self.fp_pushButton_on.clicked.connect(lambda: self.updateButtonState(Status.ATTENDANCE))
		self.fp_pushButton_out.clicked.connect(lambda: self.updateButtonState(Status.LEAVE))
		self.out_pushButton_eating.clicked.connect(lambda: self.updateButtonState(Status.EATING))
		self.out_pushButton_lib.clicked.connect(lambda: self.updateButtonState(Status.LIB))
		self.out_pushButton_else.clicked.connect(lambda: self.updateButtonState(Status.ETC))
		self.out_pushButton_return.clicked.connect(lambda: self.updateButtonState(Status.RETURN))
		self.new_pushButton_ok.clicked.connect(lambda: self.updateButtonState(Status.REGISTER))
		self.close_button.clicked.connect(lambda: self.updateButtonState(Status.CLOSE))
		
		# 초기 페이지를 출석 페이지로 설정
		self.fingerprint_button.click()

		self.showTime()

	def changeStdNum(self, num):
		"""학번 입력 처리"""
		if num == "back" and self.stdNum:
			self.stdNum = self.stdNum[:-1]
		elif num != "back":
			self.stdNum += num
			
		self.new_label_text.setText(self.stdNum if self.stdNum else "학번을 입력해주세요")

	def register_fingerprint(self):
		"""지문 등록 처리"""
		if not self.stdNum:
			self.new_label_text.setText("학번을 입력해주세요")
			return
		
		# TODO: 지문 등록 로직 구현
		self.new_label_text.setText("지문 등록 기능은 아직 구현되지 않았습니다.")

	def log(self, log_type):
		"""출석 로그 기록"""
		# TODO: 로그 기록 로직 구현
		self.new_label_text.setText(f"{log_type} 기능은 아직 구현되지 않았습니다.")

	def changePage(self, pageIndex):
		"""페이지 전환"""
		self.pages.setCurrentIndex(pageIndex)
		self.buttons = [self.fingerprint_button, self.outing_button, self.new_fingerprint_button]
		for button in self.buttons:
			button.setStyleSheet("background-color: rgb(78, 78, 78); color: rgb(227, 227, 227);")
		self.buttons[pageIndex].setStyleSheet("background-color: gray; color: rgb(227, 227, 227); border: 0px;")
		
		# 페이지 전환 시 학번 초기화
		self.stdNum = ""

		# 상태 업데이트 및 표시
		if pageIndex == 0:
			self.updateButtonState(Status.ATTENDANCE)
		elif pageIndex == 1:
			self.updateButtonState(Status.EATING)
		elif pageIndex == 2:  # 등록 페이지
			self.updateButtonState(Status.REGISTER)

	def showTime(self):
		current_date = QDateTime.currentDateTime()
		current_date = current_date.toString('yyyy-MM-dd\thh:mm:ss')
		self.fp_label_date.setText(current_date)
		self.out_label_date.setText(current_date)

		timer = Timer(1, self.showTime)
		timer.start()

	def updateButtonState(self, button_status):
		"""버튼 상태 업데이트 및 색상 강조"""
		self.buttons = {
			Status.ATTENDANCE: self.fp_pushButton_on,
			Status.LEAVE: self.fp_pushButton_out,
			Status.EATING: self.out_pushButton_eating,
			Status.LIB: self.out_pushButton_lib,
			Status.ETC: self.out_pushButton_else,
			Status.RETURN: self.out_pushButton_return,
			Status.REGISTER: self.new_pushButton_ok,
			Status.CLOSE: self.close_button
		}
		
		# 모든 버튼 색상 초기화
		for button in self.buttons.values():
			button.setStyleSheet("background-color: rgb(60, 60, 60); color: rgb(227, 227, 227);")

		self.new_pushButton_ok.setStyleSheet("background-color: rgb(50, 50, 50); color: rgb(227, 227, 227);")
		self.close_button.setStyleSheet("background-color: rgb(78, 78, 78); color: rgb(227, 227, 227);")
		
		# 선택된 버튼 색상 강조
		if button_status in self.buttons and button_status is not Status.REGISTER:
			self.buttons[button_status].setStyleSheet("background-color: gray; color: rgb(227, 227, 227); border: 0px;")
		
		# 상태 업데이트
		set_status(button_status)
		print(get_status())