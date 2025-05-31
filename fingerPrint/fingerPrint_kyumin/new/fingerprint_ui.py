import os
from PyQt5.QtCore import QDateTime, QTimer
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from status_manager import Status, get_status, set_status, get_student_id, set_student_id, set_sensor_active, clear_student_id
from threading import Timer

class FingerprintUI(QMainWindow):
	push_buttons = {}
	page_buttons = []
	
	def __init__(self):
		super().__init__()
		# UI 파일 로드
		ui_path = os.path.join(os.path.dirname(__file__), "new.ui")
		loadUi(ui_path, self)

		# 메시지 타이머 세팅
		self.message_timer = QTimer()
		self.message_timer.timeout.connect(self.clear_message)

		# 시계 타이머 세팅 및 실행
		self.clock_timer = QTimer(self)
		self.clock_timer.timeout.connect(self.showTime)
		self.clock_timer.start(1000)

		# 메시지 초기화
		self.clear_message()

		# 페이지 버튼 세팅
		self.page_buttons = [self.fingerprint_button, self.outing_button, self.new_fingerprint_button]

		# 페이지 버튼 연결
		for index, button in enumerate(self.page_buttons):
			button.clicked.connect(lambda _, i=index: self.changePage(i))
		
		# 숫자 버튼 세팅
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

		# api 버튼 세팅
		self.push_buttons = {
			Status.ATTENDANCE: self.fp_pushButton_on,
			Status.LEAVE: self.fp_pushButton_out,
			Status.EATING: self.out_pushButton_eating,
			Status.LIB: self.out_pushButton_lib,
			Status.ETC: self.out_pushButton_else,
			Status.RETURN: self.out_pushButton_return,
			Status.REGISTER: self.new_pushButton_ok,
			Status.CLOSE: self.close_button
		}
		
		# api 버튼 이벤트 연결
		for status, button in self.push_buttons.items():
			button.clicked.connect(lambda _, s=status: self.updateButtonState(s))
		
		# 초기 페이지를 출석 페이지로 설정
		self.fingerprint_button.click()

	def changeStdNum(self, num):
		"""학번 입력 처리"""
		if num == "back":
			current_id = get_student_id()
			if current_id:
				set_student_id(current_id[:-1])
		else:
			set_student_id(get_student_id() + num)

		# 대기 상태로 전환
		self.updateButtonState(Status.WAITING)
		self.set_message(get_student_id() if get_student_id() else "학번을 입력해 주세요")

	def changePage(self, pageIndex):
		"""페이지 전환"""
		self.pages.setCurrentIndex(pageIndex)

		# 선택된 페이지 버튼 강조
		for button in self.page_buttons:
			button.setStyleSheet("background-color: rgb(78, 78, 78); color: rgb(227, 227, 227); border: 0px;")
		self.page_buttons[pageIndex].setStyleSheet("background-color: gray; color: rgb(227, 227, 227); border: 0px;")
		
		# 페이지 전환 시 라벨 및 학번 초기화
		self.clear_message()
		clear_student_id()

		# 상태 업데이트 및 표시
		if pageIndex == 0:		# 등하교 페이지
			self.updateButtonState(Status.ATTENDANCE)
		elif pageIndex == 1:	# 외출 페이지
			self.updateButtonState(Status.EATING)
		elif pageIndex == 2:  	# 지문 등록 페이지
			self.updateButtonState(Status.WAITING)

	def showTime(self):
		"""시간 표시 함수"""
		current_date = QDateTime.currentDateTime()
		current_date = current_date.toString('yyyy-MM-dd\thh:mm:ss')
		self.fp_label_date.setText(current_date)
		self.out_label_date.setText(current_date)

	def updateButtonState(self, button_status):
		"""버튼 상태 업데이트 및 색상 강조"""
		
		# 모든 버튼 색상 초기화
		for button in self.push_buttons.values():
			button.setStyleSheet("background-color: rgb(60, 60, 60); color: rgb(227, 227, 227); border: 0px;")

		self.close_button.setStyleSheet("background-color: rgb(78, 78, 78); color: rgb(227, 227, 227); border: 0px;")
		
		# 선택된 버튼 색상 강조
		if button_status in self.push_buttons and button_status is not Status.REGISTER:
			self.push_buttons[button_status].setStyleSheet("background-color: gray; color: rgb(227, 227, 227); border: 0px;")
		
		# 상태 업데이트
		set_status(button_status)
		print(get_status())

		# 지문 등록 이벤트 처리
		if button_status == Status.REGISTER:
			clear_student_id()
			QTimer.singleShot(100, lambda: self.updateButtonState(Status.WAITING))
			return

	def set_message(self, text: str):
		"""세 개의 라벨에 동일한 텍스트 설정"""
		self.fp_label_text.setText(text)
		self.out_label_text.setText(text)
		self.new_label_text.setText(text)
		# 3초 후에 기본 메시지로 복귀
		self.message_timer.start(3000)  # 3000ms = 3초

	def set_info_message(self, text: str):
		"""세 개의 라벨에 동일한 텍스트 설정"""
		self.set_message(text)
		# 정보 표출 중 지문 센서 비활성화
		set_sensor_active(False)
		
	def clear_message(self):
		"""기본 메시지로 복귀 및 지문 센서 활성화"""
		self.fp_label_text.setText("지문을 인식해 주세요")
		self.out_label_text.setText("지문을 인식해 주세요")
		self.new_label_text.setText("학번을 입력해 주세요")
		self.message_timer.stop()
		set_sensor_active(True)

	def deactive_button(self):
		"""모든 버튼 비활성화"""
		# 페이지 버튼 비활성화
		for button in self.page_buttons:
			button.setEnabled(False)
		
		# 기능 버튼 비활성화
		for button in self.push_buttons.values():
			button.setEnabled(False)
		
		# 숫자 버튼 비활성화
		for i in range(10):
			button = getattr(self, f'new_pushButton_{i}')
			button.setEnabled(False)
		
		# 기타 버튼 비활성화
		self.new_pushButton_back.setEnabled(False)
		self.new_pushButton_ok.setEnabled(False)

	def active_button(self):
		"""모든 버튼 활성화"""
		# 페이지 버튼 활성화
		for button in self.page_buttons:
			button.setEnabled(True)
		
		# 기능 버튼 활성화
		for button in self.push_buttons.values():
			button.setEnabled(True)
		
		# 숫자 버튼 활성화
		for i in range(10):
			button = getattr(self, f'new_pushButton_{i}')
			button.setEnabled(True)
		
		# 기타 버튼 활성화
		self.new_pushButton_back.setEnabled(True)
		self.new_pushButton_ok.setEnabled(True)