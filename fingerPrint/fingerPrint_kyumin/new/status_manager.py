from enum import Enum

# 상태 정의
class Status(Enum):
	REGISTER = "등록"
	ATTENDANCE = "등교"
	LEAVE = "하교"
	LIB = "도서관"
	EATING = "식사"
	ETC = "기타"
	RETURN = "복귀"
	CLOSE = "문닫기"

# 전역 설정
CONFIG = {
	'use_mock': False,
	'status': Status.ATTENDANCE,  # 기본 상태는 등교
	'sensor_active': False  # 지문 인식기 활성화 상태
}

def get_status() -> Status:
	"""
	현재 애플리케이션의 상태를 반환합니다.
	
	Returns:
		Status: 현재 상태 (등교/하교/외출/등록)
	"""
	return CONFIG["status"]

def set_status(new_status: Status) -> None:
	"""
	애플리케이션의 상태를 변경합니다.
	
	Args:
		new_status (Status): 변경할 새로운 상태
	"""
	CONFIG["status"] = new_status

def is_mock() -> bool:
	"""
	현재 mock 모드 여부를 반환합니다.
	
	Returns:
		bool: mock 모드이면 True, 아니면 False
	"""
	return CONFIG["use_mock"]

def set_mock_mode(use_mock: bool) -> None:
	"""
	mock 모드를 설정합니다.
	
	Args:
		use_mock (bool): mock 모드 사용 여부
	"""
	CONFIG["use_mock"] = use_mock

def is_sensor_active() -> bool:
	"""
	지문 인식기 활성화 상태를 반환합니다.
	
	Returns:
		bool: 지문 인식기가 활성화되어 있으면 True, 아니면 False
	"""
	return CONFIG["sensor_active"]

def set_sensor_active(active: bool) -> None:
	"""
	지문 인식기 활성화 상태를 설정합니다.
	
	Args:
		active (bool): 지문 인식기 활성화 여부
	"""
	CONFIG["sensor_active"] = active 