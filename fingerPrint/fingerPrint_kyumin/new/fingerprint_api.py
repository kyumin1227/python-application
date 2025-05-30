from status_manager import get_status, Status, is_mock
import requests
import os
from PyQt5.QtCore import QObject, pyqtSignal
import time

# 전역 변수
SERVER_URL = None
SERVER_KEY = None

class APIMessageHandler(QObject):
	message = pyqtSignal(str)
	
api_message = APIMessageHandler()

def init_api():
	global SERVER_URL
	global SERVER_KEY
	
	SERVER_URL = os.getenv("FP_URL")
	SERVER_KEY = os.getenv("FP_KEY")

def get_all_fingerprint_data():
	"""모든 지문 정보를 가져와서 반환"""
	api_message.message.emit(SERVER_URL)
	try:
		response = requests.get(
			f"{SERVER_URL}/students",
			headers={"Authorization": f"Bearer {SERVER_KEY}"}
		)
		
		if response.status_code == 200:
			data = response.json()
			api_message.message.emit("지문 정보를 성공적으로 가져왔습니다.")
			return data["data"]
		else:
			api_message.message.emit("지문 정보를 가져오는데 실패했습니다.")
			return []
			
	except Exception as e:
		api_message.message.emit(f"지문 정보 조회 중 오류 발생: {str(e)}")
		return []

def check_student_registration(student_id: str) -> bool:
	"""가입 가능한 학번인지 검증"""
	api_message.message.emit("test")
	print("check")
	try:
		response = requests.get(
			f"{SERVER_URL}/students/{student_id}",
			headers={"Authorization": f"Bearer {SERVER_KEY}"}
		)
		
		if response.status_code == 200:
			response_data = response.json()
			if response_data.get("success"):
				api_message.message.emit(response_data.get("message", "가입 가능한 학번입니다."))
				return True
			else:
				api_message.message.emit(response_data.get("message", "가입할 수 없는 학번입니다."))
				return False
		else:
			response_data = response.json()
			api_message.message.emit(response_data.get("message", "가입할 수 없는 학번입니다."))
			return False
			
	except Exception as e:
		api_message.message.emit(f"학번 검증 중 오류 발생: {str(e)}")
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
		if response.status_code == 200:
			api_message.message.emit("지문 등록이 완료되었습니다.")
			return True
		else:
			api_message.message.emit("지문 등록에 실패했습니다.")
			return False
	except Exception as e:
		api_message.message.emit(f"지문 등록 중 오류 발생: {str(e)}")
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
		if response.status_code == 200:
			response_data = response.json()
			api_message.message.emit(response_data.get("message", "문이 닫혔습니다."))
			return True
		else:
			response_data = response.json()
			api_message.message.emit(response_data.get("message", "문 닫기에 실패했습니다."))
			return False
	except Exception as e:
		api_message.message.emit(f"문 닫기 중 오류 발생: {str(e)}")
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
		if response.status_code == 200:
			response_data = response.json()
			api_message.message.emit(response_data.get("message", "로그가 기록되었습니다."))
			return True
		else:
			api_message.message.emit("로그 기록에 실패했습니다.")
			return False
	except Exception as e:
		api_message.message.emit(f"로그 기록 중 오류 발생: {str(e)}")
		return False 