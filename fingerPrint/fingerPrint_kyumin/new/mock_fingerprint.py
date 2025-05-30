import time

class MockFingerprint:
    def __init__(self, port, baudrate, address, password):
        self.templates = []
        self.current_image = None
        self.characteristics = None
        self.template_index = 0

    def clearDatabase(self):
        print("fingerprint clear")
        self.templates = []
        self.template_index = 0
        return True

    def readImage(self):
        # 실제 지문 인식기에서는 지문을 읽어오는 동작을 수행
        # Mock에서는 항상 성공으로 가정
        print("fingerprint read")
        time.sleep(1)

        return True

    def convertImage(self, charBufferId):
        # 실제 지문 인식기에서는 이미지를 특성점으로 변환
        # Mock에서는 더미 데이터 생성
        self.characteristics = [0] * 512
        return True

    def searchTemplate(self):
        # 실제 지문 인식기에서는 저장된 템플릿과 비교
        # Mock에서는 항상 첫 번째 템플릿과 매칭되는 것으로 가정
        if len(self.templates) > 0:
            return (0, 100)  # (인덱스, 매칭 점수)
        return (-1, 0)

    def uploadCharacteristics(self, charBufferId, characteristics):
        self.characteristics = characteristics
        return True

    def downloadCharacteristics(self, charBufferId):
        return self.characteristics

    def createTemplate(self):
        # 실제 지문 인식기에서는 특성점으로부터 템플릿 생성
        # Mock에서는 더미 템플릿 생성
        self.template = [0] * 512
        return True

    def storeTemplate(self):
        # 실제 지문 인식기에서는 템플릿을 저장
        # Mock에서는 템플릿 리스트에 추가
        self.templates.append(self.template)
        self.template_index += 1
        return True 