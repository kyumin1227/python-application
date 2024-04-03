# fingerprint 코드를 MAC 환경에서 돌리기 위한 Mock 코드
from unittest.mock import Mock

# mock 객체 생성
mock_object = Mock()

mock_object.getTemplateCount.return_value = 10