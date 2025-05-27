from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTime, QDateTime, Qt, QThread
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from threading import Timer
import time
import base64
import requests
import os, json, sys

# 명령줄 인자 확인
USE_MOCK = len(sys.argv) > 1 and sys.argv[1] == "mock"

if USE_MOCK:
	from mock_fingerprint import MockFingerprint as PyFingerprint
	PASSWORD = "123".encode("utf-8")
	SERVER_URL = "http://210.101.236.158:8081/api/fingerprint"
	SERVER_KEY = ""
else:
	from pyfingerprint.pyfingerprint import PyFingerprint
	PASSWORD = os.getenv("FP_PASSWORD").encode("utf-8")	# 암호화 시 사용하는 비밀번호
	SERVER_URL = os.getenv("FP_URL")	# 서버 주소
	SERVER_KEY = os.getenv("FP_KEY")	# 서버에 전달하는 키

# 상수 정의
headers = {
    'Content-Type': 'application/json'
}

# 키 생성 함수
def generate_key(password, salt):
	kdf = PBKDF2HMAC(
		algorithm=hashes.SHA256(),
		length=32,
		salt=salt,
		iterations=100000,
		backend=default_backend()
	)
	return kdf.derive(password)

# 암호화 함수
def encrypt(data, key):
	iv = os.urandom(16)  # 초기화 벡터 생성
	cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
	encryptor = cipher.encryptor()
	encrypted_data = encryptor.update(data) + encryptor.finalize()
	return iv + encrypted_data  # IV와 암호화된 데이터를 함께 반환

# 복호화 함수
def decrypt(encrypted_data, key):
	iv = encrypted_data[:16]  # IV 추출
	encrypted_data = encrypted_data[16:]  # 실제 암호화된 데이터
	cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
	decryptor = cipher.decryptor()
	return decryptor.update(encrypted_data) + decryptor.finalize()

def decode_and_decrypt(encoded_data: str, salt_b64: str) -> list:
	raw_data = base64.b64decode(encoded_data.encode("utf-8"))
	salt = base64.b64decode(salt_b64.encode("utf-8"))
	key = generate_key(PASSWORD, salt)
	decrypted = decrypt(raw_data, key)
	return list(decrypted)

def getFingerList(f):
	res = requests.get(SERVER_URL + "/students")
	jsonData = res.json()
	dataList = jsonData["data"]
	for data in dataList:
		fpData1 = decode_and_decrypt(data["fingerPrintImage1"], data["salt"])
		fpData2 = decode_and_decrypt(data["fingerPrintImage2"], data["salt"])

		f.uploadCharacteristics(0x01, fpData1)
		f.uploadCharacteristics(0x02, fpData2)
		f.createTemplate()
		f.storeTemplate()

		STUDENT_LIST.append(data["studentNumber"])
          
def connect_fingerprint():
	try:
		f = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)
	except Exception as e:
		print("지문 인식기 연결 실패", e)
		exit(1)
	else:
		print("지문 인식기 연결 성공")
	return f

class FingerprintUI(QMainWindow):
	def __init__(self):
		super().__init__()
		# UI 파일 로드
		loadUi("qt-designer/new.ui", self)
		
		# 변수 초기화
		self.stdNum = ""
		self.activate = False
		self.start_time = 0
		self.fpData1 = None
		self.fpData2 = None
		
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
		self.new_pushButton_ok.clicked.connect(self.register_fingerprint)
		self.fp_pushButton_on.clicked.connect(lambda: self.log("등교"))
		self.fp_pushButton_out.clicked.connect(lambda: self.log("하교"))
		self.out_pushButton_gohan.clicked.connect(lambda: self.log("식사"))
		self.out_pushButton_lib.clicked.connect(lambda: self.log("도서관"))
		self.out_pushButton_else.clicked.connect(lambda: self.log("기타"))
		self.out_pushButton_return.clicked.connect(lambda: self.log("복귀"))
		self.new_pushButton_ok.clicked.connect(lambda: self.data("create"))
		
		# 초기 페이지를 출석 페이지로 설정
		self.fingerprint_button.click()

	def changeStdNum(self, num):
		"""학번 입력 처리"""
		print(num)
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

		# 학번 체크
		try:
			res = requests.get(f"{SERVER_URL}/students/{self.stdNum}")
			if res.status_code == 204:
				self.new_label_text.setText("가입되지 않은 학번입니다.")
				self.stdNum = ""
				return
				
			if not res.json()["success"]:
				self.new_label_text.setText(res.json()["message"])
				self.stdNum = ""
				return
				
			# 지문 등록 시작
			self.new_label_text.setText("지문을 인식해주세요")
			self.activate = True
			self.start_time = time.time()
			
			# 여기에 지문 인식 로직 추가
			# TODO: 실제 지문 인식기 연동
			
			self.new_label_text.setText("지문 등록이 완료되었습니다.")
			self.stdNum = ""
			
		except Exception as e:
			self.new_label_text.setText(f"오류가 발생했습니다: {str(e)}")
			self.stdNum = ""
			
    # 페이지 전환 함수
	def changePage(self, pageIndex):
		self.pages.setCurrentIndex(pageIndex)
		self.buttons = [self.fingerprint_button, self.outing_button, self.new_fingerprint_button]
		for button in self.buttons:
			button.setStyleSheet("background-color: rgb(78, 78, 78); color: rgb(227, 227, 227); border: 0px;")
		self.buttons[pageIndex].setStyleSheet("background-color: gray; color: rgb(227, 227, 227); border: 0px;")
		
		# 페이지 전환 시 학번 초기화
		self.stdNum = ""
		# self.clear_label_text()
	

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = FingerprintUI()
	window.showFullScreen()
	sys.exit(app.exec_())
