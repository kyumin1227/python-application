from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from PyQt5.QtCore import QThread, pyqtSignal
from status_manager import is_mock, get_status, is_sensor_active, Status, get_student_id
from fingerprint_api import get_all_fingerprint_data, check_student_registration, register_fingerprint, log_status, close_door
import time
import base64
import os

MATCH_THRESHOLD = 50	# 동일 지문 판단 기준

class FingerprintSensor(QThread):
	# 지문 감지 시그널
	message = pyqtSignal(str)  # 지문 템플릿을 전달

	def __init__(self):
		super().__init__()
		self.running = True
		self.PASSWORD = None
		self.STUDENT_LIST = []

		# 환경 변수 및 모듈 초기화
		if is_mock():
			from mock_fingerprint import MockFingerprint as PyFingerprint
			self.PASSWORD = "123".encode("utf-8")
		else:
			from pyfingerprint.pyfingerprint import PyFingerprint
			self.PASSWORD = os.getenv("FP_PASSWORD").encode("utf-8")	# 암호화 시 사용하는 비밀번호

		# 센서 초기화
		try:
			self.sensor = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)
			print("지문 인식기 연결 성공")
		except Exception as e:
			print("지문 인식기 연결 실패:", e)
			self.message.emit(str(e))

		if not is_mock():
			self.getFingerList()

	def run(self):
		"""스레드에서 실행될 메인 로직"""
		while self.running:

			self.scan_fingerprint()

	def scan_fingerprint(self):
		"""지문 스캔 처리"""
		try:
			# 센서가 비활성화 상태면 None 반환
			if not is_sensor_active():
				return

			current_status = get_status()
			
			if current_status == Status.REGISTER:
				return self.register_fingerprint()
			else:
				return self.verify_fingerprint(current_status)
					
		except Exception as e:
			self.message.emit(f"지문 스캔 중 오류 발생: {str(e)}")

	def register_fingerprint(self):
		"""지문 등록 처리"""
		student_id = get_student_id()
		if not check_student_registration(student_id):
			return

		start_time = time.time()

		while time.time() - start_time < 5:
			if self.sensor.readImage() != False:
				self.sensor.convertImage(0x01)
				break

		self.message.emit("첫 번째 지문이 등록되었습니다. \n두 번째 지문을 스캔해주세요.")
		start_time = time.time()

		while time.time() - start_time < 5:
			if self.sensor.readImage() != False:
				self.sensor.convertImage(0x02)
				break

		if self.sensor.compareCharacteristics() == 0:
			self.message.emit("등록한 지문이 일치하지 않습니다.")
			return None

		raw_salt = os.urandom(16)
		key = self.generate_key(self.PASSWORD, raw_salt)

		fp_data1 = self.encode_and_encrypt(0x01, key)
		fp_data2 = self.encode_and_encrypt(0x02, key)
		salt = base64.b64encode(raw_salt).decode("utf-8")

		# API 호출하여 지문 데이터 전송
		if register_fingerprint(student_id, fp_data1, fp_data2, salt):
			self.create_and_store_template(student_id)

	def verify_fingerprint(self, current_status: Status):
		"""지문 검증 처리"""

		if self.sensor.readImage() != False:
			self.sensor.convertImage(0x01)
			result = self.sensor.searchTemplate()
			
			if result[0] >= 0 and result[1] >= MATCH_THRESHOLD:
				# 일치하는 지문을 찾았을 때
				student_id = self.STUDENT_LIST[result[0]]

				if current_status == Status.CLOSE:
					# 문 닫기 API 호출
					close_door(student_id)
					return
				
				# 로그 API 호출
				log_status(student_id, current_status)

	def stop(self):
		"""스레드 종료"""
		self.running = False
		self.wait()

	def generate_key(self, password, salt):
		"""암호화 키 생성"""
		kdf = PBKDF2HMAC(
			algorithm=hashes.SHA256(),
			length=32,
			salt=salt,
			iterations=100000,
			backend=default_backend()
		)
		return kdf.derive(password)

	def encrypt(self, data, key):
		"""데이터 암호화"""
		iv = os.urandom(16)  # 초기화 벡터 생성
		cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
		encryptor = cipher.encryptor()
		encrypted_data = encryptor.update(data) + encryptor.finalize()
		return iv + encrypted_data  # IV와 암호화된 데이터를 함께 반환

	def decrypt(self, encrypted_data, key):
		"""데이터 복호화"""
		iv = encrypted_data[:16]  # IV 추출
		encrypted_data = encrypted_data[16:]  # 실제 암호화된 데이터
		cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
		decryptor = cipher.decryptor()
		return decryptor.update(encrypted_data) + decryptor.finalize()
	
	def encode_and_encrypt(self, charBufferId, key):
		"""데이터 암호화 및 인코딩"""
		fingerprint_data = bytes(self.sensor.downloadCharacteristics(charBufferId))
		encrypted_data = self.encrypt(fingerprint_data, key)
		encoded_data = base64.b64encode(encrypted_data)
		return encoded_data

	def decode_and_decrypt(self, encoded_data: str, salt_b64: str) -> list:
		"""인코딩된 데이터 복호화"""
		raw_data = base64.b64decode(encoded_data.encode("utf-8"))
		salt = base64.b64decode(salt_b64.encode("utf-8"))
		key = self.generate_key(self.PASSWORD, salt)
		decrypted = self.decrypt(raw_data, key)
		return list(decrypted)

	def getFingerList(self):
		"""서버에서 지문 데이터 가져오기"""
		self.sensor.clearDatabase()
		self.STUDENT_LIST.clear()
		dataList = get_all_fingerprint_data()
		for data in dataList:
			fpData1 = self.decode_and_decrypt(data["fingerPrintImage1"], data["salt"])
			fpData2 = self.decode_and_decrypt(data["fingerPrintImage2"], data["salt"])

			self.sensor.uploadCharacteristics(0x01, fpData1)
			self.sensor.uploadCharacteristics(0x02, fpData2)
			self.create_and_store_template(data["studentNumber"])

	def create_and_store_template(self, student_number):
		"""버퍼의 지문 데이터 지문 인식기에 저장"""
		self.sensor.createTemplate()
		self.sensor.storeTemplate()
		self.STUDENT_LIST.append(student_number)