from status_manager import Status
import requests
import os
from PyQt5.QtCore import QObject, pyqtSignal
from status_manager import is_mock
import sys

# 전역 변수
SERVER_URL = "http://210.101.236.158:8081/api/fingerprint"
SERVER_KEY = "dev"

class APIMessageHandler(QObject):
	message = pyqtSignal(str)
	
api_message = APIMessageHandler()

def init_api():
	global SERVER_URL
	global SERVER_KEY

	if not is_mock():
		try:
			SERVER_URL = os.getenv("FP_URL")
			SERVER_KEY = os.getenv("FP_KEY")

			if SERVER_URL is None:
				raise ValueError("FP_URL 환경 변수가 설정되지 않았습니다.")
			if SERVER_KEY is None:
				raise ValueError("FP_KEY 환경 변수가 설정되지 않았습니다.")
		except ValueError as e:
			print(e)
			sys.exit(1)

def get_all_fingerprint_data():
	"""모든 지문 정보를 가져와서 반환"""
	api_message.message.emit(SERVER_URL)
	try:
		response = requests.get(
			f"{SERVER_URL}/students",
			headers={"Authorization": f"Bearer {SERVER_KEY}"}
		)
		if handle_api_response(response):
			return response.json()["data"]
		else:
			return []
	except requests.exceptions as e:
		api_message.message.emit(f"요청 과정에서 오류 발생\n{str(e)}")
		return []
	except Exception as e:
		api_message.message.emit(f"지문 정보 조회 중 오류 발생\n{str(e)}")
		return []

def check_student_registration(student_id: str) -> bool:
	"""가입 가능한 학번인지 검증"""
	try:
		response = requests.get(
			f"{SERVER_URL}/students/{student_id}",
			headers={"Authorization": f"Bearer {SERVER_KEY}"}
		)
		return handle_api_response(response)
	except Exception as e:
		api_message.message.emit(f"학번 검증 중 오류 발생\n{str(e)}")
		return False

def register_fingerprint(student_id: str, fp_data1, fp_data2, salt):
	"""지문 등록 API 호출"""
	try:
		response = requests.post(
			f"{SERVER_URL}/students",
			headers={"Authorization": f"Bearer {SERVER_KEY}"},
			json={
				"fingerprint1": fp_data1,
				"fingerprint2": fp_data2,
				"std_num": student_id,
				"salt": salt
            }
		)
		return handle_api_response(response)
	except Exception as e:
		api_message.message.emit(f"지문 등록 중 오류 발생\n{str(e)}")
		return False

def close_door(student_id: str):
	"""문 닫기 API 호출"""
	try:
		response = requests.post(
			f"{SERVER_URL}/close",
			headers={"Authorization": f"Bearer {SERVER_KEY}"},
			json={
				"closingMember": student_id
			}
		)
		return handle_api_response(response)
	except Exception as e:
		api_message.message.emit(f"문 닫기 중 오류 발생\n{str(e)}")
		return False

def log_status(student_id: str, status: Status):
	"""로그 API 호출"""
	try:
		response = requests.post(
			f"{SERVER_URL}/logs",
			headers={"Authorization": f"Bearer {SERVER_KEY}"},
			json={
				"std_num": student_id,
				"action": status.value
			}
		)
		return handle_api_response(response)
	except Exception as e:
		api_message.message.emit(f"로그 기록 중 오류 발생\n{str(e)}")
		return False
	
def handle_api_response(response) -> bool:
	"""API 응답을 처리 후 응답 데이터를 반환"""
	try:
		response_data = response.json()
		if response.status_code == 200 or response.status_code == 400:
			api_message.message.emit(response_data["message"])
			return response_data["success"]
		elif response.status_code == 404:
			api_message.message.emit("404, 엔드포인트를 찾을 수 없습니다.")
			return False
		
	except KeyError as e:
		api_message.message.emit("응답 형식이 올바르지 않습니다.")
		return False
	except Exception as e:
		api_message.message.emit(f"오류 발생\n{str(e)}")
		return False