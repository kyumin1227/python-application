from enum import Enum

# 상태 정의
class Status(Enum):
	WAITING = "대기"
	REGISTER = "등록"
	ATTENDANCE = "등교"
	LEAVE = "하교"
	LIB = "도서관"
	EATING = "식사"
	ETC = "기타"
	RETURN = "복귀"
	CLOSE = "문닫기"

# 전역 설정 변수
use_mock = False
status = Status.ATTENDANCE  # 기본 상태는 등교
sensor_active = False  # 지문 인식기 활성화 상태
student_id = ""  # 현재 입력된 학번

def get_status() -> Status:
	"""
	현재 애플리케이션의 상태를 반환합니다.
	
	Returns:
		Status: 현재 상태 (등교/하교/외출/등록)
	"""
	return status

def set_status(new_status: Status) -> None:
	"""
	애플리케이션의 상태를 변경합니다.
	WAITING 상태일 때는 센서를 비활성화하고,
	다른 상태일 때는 센서를 활성화합니다.
	
	Args:
		new_status (Status): 변경할 새로운 상태
	"""
	global status
	status = new_status
	
	# 상태에 따라 센서 활성화 상태 자동 변경
	if new_status == Status.WAITING:
		set_sensor_active(False)
	elif new_status == Status.REGISTER:
		set_sensor_active(True)
	else:
		set_sensor_active(True)
		clear_student_id()

def is_mock() -> bool:
	"""
	현재 mock 모드 여부를 반환합니다.
	
	Returns:
		bool: mock 모드이면 True, 아니면 False
	"""
	return use_mock

def set_mock_mode(use_mock_mode: bool) -> None:
	"""
	mock 모드를 설정합니다.
	
	Args:
		use_mock_mode (bool): mock 모드 사용 여부
	"""
	global use_mock
	use_mock = use_mock_mode

def is_sensor_active() -> bool:
	"""
	지문 인식기 활성화 상태를 반환합니다.
	
	Returns:
		bool: 지문 인식기가 활성화되어 있으면 True, 아니면 False
	"""
	return sensor_active

def set_sensor_active(active: bool) -> None:
	"""
	지문 인식기 활성화 상태를 설정합니다.
	
	Args:
		active (bool): 지문 인식기 활성화 여부
	"""
	global sensor_active
	sensor_active = active

def get_student_id() -> str:
	"""
	현재 입력된 학번을 반환합니다.
	
	Returns:
		str: 현재 입력된 학번
	"""
	return student_id

def set_student_id(new_student_id: str) -> None:
	"""
	학번을 설정합니다.
	
	Args:
		new_student_id (str): 설정할 학번
	"""
	global student_id
	student_id = new_student_id

def clear_student_id() -> None:
	"""
	학번을 초기화합니다.
	"""
	global student_id
	student_id = "" 