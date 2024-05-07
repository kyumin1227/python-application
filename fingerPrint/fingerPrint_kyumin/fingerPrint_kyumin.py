# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './fingerPrint/fingerPrint_kyumin/qt-designer/ammend_2.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

# 페이지는 4개 존재하며 각각의 페이지 내부의 요소들은 이름의 앞에 통일된 글자를 추가
# fingerPrint(출석): fp
# outing(외출): out
# new_fingerPrint(지문 등록): new
# delete_fingerPrint(지문 삭제): delete

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTime, QDateTime, Qt, QThread
from threading import Timer
import time
import base64
import requests
import os, json

from pyfingerprint.pyfingerprint import PyFingerprint

PASSWORD = os.getenv("FP_PASSWORD")	# 암호화 시 사용하는 비밀번호
SERVER_URL = os.getenv("FP_URL")	# 서버 주소
SERVER_KEY = os.getenv("FP_KEY")	# 서버에 전달하는 키

try:
	f = PyFingerprint('/dev/ttyAMA0', 57600, 0xFFFFFFFF, 0x00000000)
except Exception as e:
	print("지문 인식기 연결 실패", e)
	exit(1)
else:
	print("지문 인식기 연결 성공")

time.sleep(1)
f.clearDatabase()

# 새로운 지문 정보 등록시 보낼 딕셔너리
new_fingerprint_dic = {
	"fingerprint1": "",
	"fingerprint2": "",
	"std_num": "",
	"salt": ""
}

class Ui_MainWindow(object):
	def __init__(self):
		self.action = ""
		self.activate = False
		self.stdNum = ""

	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(811, 480)
		MainWindow.setAutoFillBackground(False)
		MainWindow.setStyleSheet("background-color: rgb(50, 50, 50);")
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.fingerprint_button = QtWidgets.QPushButton(self.centralwidget)
		self.fingerprint_button.setGeometry(QtCore.QRect(40, 40, 120, 95))
		self.fingerprint_button.setStyleSheet("background-color: rgb(78, 78, 78);\n"
"color: rgb(227, 227, 227); border: 0px;")
		self.fingerprint_button.setObjectName("fingerprint_button")
		self.fingerprint_button.clicked.connect(lambda: self.changePage(0))
		self.outing_button = QtWidgets.QPushButton(self.centralwidget)
		self.outing_button.setGeometry(QtCore.QRect(40, 140, 120, 95))
		self.outing_button.setStyleSheet("background-color: rgb(78, 78, 78);\n"
"color: rgb(227, 227, 227); border: 0px;")
		self.outing_button.setObjectName("outing_button")
		self.outing_button.clicked.connect(lambda: self.changePage(1))
		self.new_fingerprint_button = QtWidgets.QPushButton(self.centralwidget)
		self.new_fingerprint_button.setGeometry(QtCore.QRect(40, 240, 120, 95))
		self.new_fingerprint_button.setStyleSheet("background-color: rgb(78, 78, 78);\n"
"color: rgb(227, 227, 227); border: 0px;")
		self.new_fingerprint_button.setObjectName("new_fingerprint_button")
		self.new_fingerprint_button.clicked.connect(lambda: self.changePage(2))
		self.delete_fingerprint_button = QtWidgets.QPushButton(self.centralwidget)
		self.delete_fingerprint_button.setGeometry(QtCore.QRect(40, 340, 120, 95))
		self.delete_fingerprint_button.setStyleSheet("background-color: rgb(78, 78, 78);\n"
"color: rgb(227, 227, 227); border: 0px;")
		self.delete_fingerprint_button.setObjectName("delete_fingerprint_button")
		self.delete_fingerprint_button.clicked.connect(lambda: self.changePage(3))
		self.pages = QtWidgets.QStackedWidget(self.centralwidget)
		self.pages.setGeometry(QtCore.QRect(180, 40, 611, 391))
		self.pages.setAutoFillBackground(False)
		self.pages.setObjectName("pages")
		self.fingerprint_page = QtWidgets.QWidget()
		self.fingerprint_page.setObjectName("fingerprint_page")
		self.fp_label_date = QtWidgets.QLabel(self.fingerprint_page)
		self.fp_label_date.setGeometry(QtCore.QRect(40, 0, 521, 101))
		self.fp_label_date.setAutoFillBackground(False)
		self.fp_label_date.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(30, 30, 30);   \n"
"border: 1px solid rgb(70, 70, 70);\n"
"font-size: 35px;")
		self.fp_label_date.setAlignment(QtCore.Qt.AlignCenter)
		self.fp_label_date.setObjectName("fp_label_date")
		self.fp_label_now = QtWidgets.QLabel(self.fingerprint_page)
		self.fp_label_now.setGeometry(QtCore.QRect(350, 135, 211, 121))
		self.fp_label_now.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(30, 30, 30);   \n"
"border: 1px solid rgb(70, 70, 70);\n"
"font-size: 20px;")
		self.fp_label_now.setAlignment(QtCore.Qt.AlignCenter)
		self.fp_label_now.setObjectName("fp_label_now")
		self.fp_label_text = QtWidgets.QLabel(self.fingerprint_page)
		self.fp_label_text.setGeometry(QtCore.QRect(40, 290, 521, 101))
		self.fp_label_text.setAutoFillBackground(False)
		self.fp_label_text.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(30, 30, 30);   \n"
"border: 1px solid rgb(70, 70, 70);\n"
"font-size: 25px;")
		self.fp_label_text.setAlignment(QtCore.Qt.AlignCenter)
		self.fp_label_text.setObjectName("fp_label_text")
		self.fp_pushButton_on = QtWidgets.QPushButton(self.fingerprint_page)
		self.fp_pushButton_on.setGeometry(QtCore.QRect(50, 135, 121, 121))
		self.fp_pushButton_on.setStyleSheet("background-color: rgb(60, 60, 60);\n"
"color: rgb(227, 227, 227); border: 0.5px solid rgb(70, 70, 70);")
		self.fp_pushButton_on.setObjectName("fp_pushButton_on")
		self.fp_pushButton_out = QtWidgets.QPushButton(self.fingerprint_page)
		self.fp_pushButton_out.setGeometry(QtCore.QRect(175, 135, 121, 121))
		self.fp_pushButton_out.setStyleSheet("background-color: rgb(60, 60, 60);\n"
"color: rgb(227, 227, 227); border: 0.5px solid rgb(70, 70, 70);")
		self.fp_pushButton_out.setObjectName("fp_pushButton_out")
		self.pages.addWidget(self.fingerprint_page)
		self.outing_page = QtWidgets.QWidget()
		self.outing_page.setObjectName("outing_page")
		self.out_label_date = QtWidgets.QLabel(self.outing_page)
		self.out_label_date.setGeometry(QtCore.QRect(40, 0, 521, 101))
		self.out_label_date.setAutoFillBackground(False)
		self.out_label_date.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(30, 30, 30);   \n"
"border: 1px solid rgb(70, 70, 70);\n"
"font-size: 35px;")
		self.out_label_date.setAlignment(QtCore.Qt.AlignCenter)
		self.out_label_date.setObjectName("out_label_date")
		self.out_label_now = QtWidgets.QLabel(self.outing_page)
		self.out_label_now.setGeometry(QtCore.QRect(350, 135, 211, 121))
		self.out_label_now.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(30, 30, 30);   \n"
"border: 1px solid rgb(70, 70, 70);\n"
"font-size: 20px;")
		self.out_label_now.setAlignment(QtCore.Qt.AlignCenter)
		self.out_label_now.setObjectName("out_label_now")
		self.out_label_text = QtWidgets.QLabel(self.outing_page)
		self.out_label_text.setGeometry(QtCore.QRect(40, 290, 521, 101))
		self.out_label_text.setAutoFillBackground(False)
		self.out_label_text.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(30, 30, 30);   \n"
"border: 1px solid rgb(70, 70, 70);\n"
"font-size: 25px;")
		self.out_label_text.setAlignment(QtCore.Qt.AlignCenter)
		self.out_label_text.setObjectName("out_label_text")
		self.out_pushButton_gohan = QtWidgets.QPushButton(self.outing_page)
		self.out_pushButton_gohan.setGeometry(QtCore.QRect(50, 135, 121, 57))
		self.out_pushButton_gohan.setStyleSheet("background-color: rgb(60, 60, 60);\n"
"color: rgb(227, 227, 227); border: 0.5px solid rgb(70, 70, 70);")
		self.out_pushButton_gohan.setObjectName("out_pushButton_gohan")
		self.out_pushButton_lib = QtWidgets.QPushButton(self.outing_page)
		self.out_pushButton_lib.setGeometry(QtCore.QRect(175, 135, 121, 57))
		self.out_pushButton_lib.setStyleSheet("background-color: rgb(60, 60, 60);\n"
"color: rgb(227, 227, 227); border: 0.5px solid rgb(70, 70, 70);")
		self.out_pushButton_lib.setObjectName("out_pushButton_lib")
		self.out_pushButton_return = QtWidgets.QPushButton(self.outing_page)
		self.out_pushButton_return.setGeometry(QtCore.QRect(50, 200, 121, 57))
		self.out_pushButton_return.setStyleSheet("background-color: rgb(60, 60, 60);\n"
"color: rgb(227, 227, 227); border: 0.5px solid rgb(70, 70, 70);")
		self.out_pushButton_return.setObjectName("out_pushButton_walk")
		self.out_pushButton_else = QtWidgets.QPushButton(self.outing_page)
		self.out_pushButton_else.setGeometry(QtCore.QRect(175, 200, 121, 57))
		self.out_pushButton_else.setStyleSheet("background-color: rgb(60, 60, 60);\n"
"color: rgb(227, 227, 227); border: 0.5px solid rgb(70, 70, 70);")
		self.out_pushButton_else.setObjectName("out_pushButton_else")
		self.pages.addWidget(self.outing_page)
		self.new_fingerprint_page = QtWidgets.QWidget()
		self.new_fingerprint_page.setObjectName("new_fingerprint_page")
		self.new_pushButton_1 = QtWidgets.QPushButton(self.new_fingerprint_page)
		self.new_pushButton_1.setGeometry(QtCore.QRect(10, 180, 100, 100))
		self.new_pushButton_1.setStyleSheet("background-color: rgb(60, 60, 60);\n"
"color: rgb(227, 227, 227); border: 0.5px solid rgb(70, 70, 70);")
		self.new_pushButton_1.setObjectName("new_pushButton_1")
		self.new_pushButton_2 = QtWidgets.QPushButton(self.new_fingerprint_page)
		self.new_pushButton_2.setGeometry(QtCore.QRect(110, 180, 100, 100))
		self.new_pushButton_2.setStyleSheet("background-color: rgb(60, 60, 60);\n"
"color: rgb(227, 227, 227); border: 0.5px solid rgb(70, 70, 70);")
		self.new_pushButton_2.setObjectName("new_pushButton_2")
		self.new_pushButton_3 = QtWidgets.QPushButton(self.new_fingerprint_page)
		self.new_pushButton_3.setGeometry(QtCore.QRect(210, 180, 100, 100))
		self.new_pushButton_3.setStyleSheet("background-color: rgb(60, 60, 60);\n"
"color: rgb(227, 227, 227); border: 0.5px solid rgb(70, 70, 70);")
		self.new_pushButton_3.setObjectName("new_pushButton_3")
		self.new_pushButton_4 = QtWidgets.QPushButton(self.new_fingerprint_page)
		self.new_pushButton_4.setGeometry(QtCore.QRect(310, 180, 100, 100))
		self.new_pushButton_4.setStyleSheet("background-color: rgb(60, 60, 60);\n"
"color: rgb(227, 227, 227); border: 0.5px solid rgb(70, 70, 70);")
		self.new_pushButton_4.setObjectName("new_pushButton_4")
		self.new_pushButton_5 = QtWidgets.QPushButton(self.new_fingerprint_page)
		self.new_pushButton_5.setGeometry(QtCore.QRect(410, 180, 100, 100))
		self.new_pushButton_5.setStyleSheet("background-color: rgb(60, 60, 60);\n"
"color: rgb(227, 227, 227); border: 0.5px solid rgb(70, 70, 70);")
		self.new_pushButton_5.setObjectName("new_pushButton_5")
		self.new_pushButton_back = QtWidgets.QPushButton(self.new_fingerprint_page)
		self.new_pushButton_back.setGeometry(QtCore.QRect(510, 180, 100, 100))
		self.new_pushButton_back.setStyleSheet("background-color: rgb(60, 60, 60);\n"
"color: rgb(227, 227, 227); border: 0.5px solid rgb(70, 70, 70);")
		self.new_pushButton_back.setObjectName("new_pushButton_back")
		self.new_pushButton_6 = QtWidgets.QPushButton(self.new_fingerprint_page)
		self.new_pushButton_6.setGeometry(QtCore.QRect(10, 290, 100, 100))
		self.new_pushButton_6.setStyleSheet("background-color: rgb(60, 60, 60);\n"
"color: rgb(227, 227, 227); border: 0.5px solid rgb(70, 70, 70);")
		self.new_pushButton_6.setObjectName("new_pushButton_6")
		self.new_pushButton_7 = QtWidgets.QPushButton(self.new_fingerprint_page)
		self.new_pushButton_7.setGeometry(QtCore.QRect(110, 290, 100, 100))
		self.new_pushButton_7.setStyleSheet("background-color: rgb(60, 60, 60);\n"
"color: rgb(227, 227, 227); border: 0.5px solid rgb(70, 70, 70);")
		self.new_pushButton_7.setObjectName("new_pushButton_7")
		self.new_pushButton_8 = QtWidgets.QPushButton(self.new_fingerprint_page)
		self.new_pushButton_8.setGeometry(QtCore.QRect(210, 290, 100, 100))
		self.new_pushButton_8.setStyleSheet("background-color: rgb(60, 60, 60);\n"
"color: rgb(227, 227, 227); border: 0.5px solid rgb(70, 70, 70);")
		self.new_pushButton_8.setObjectName("new_pushButton_8")
		self.new_pushButton_9 = QtWidgets.QPushButton(self.new_fingerprint_page)
		self.new_pushButton_9.setGeometry(QtCore.QRect(310, 290, 100, 100))
		self.new_pushButton_9.setStyleSheet("background-color: rgb(60, 60, 60);\n"
"color: rgb(227, 227, 227); border: 0.5px solid rgb(70, 70, 70);")
		self.new_pushButton_9.setObjectName("new_pushButton_9")
		self.new_pushButton_0 = QtWidgets.QPushButton(self.new_fingerprint_page)
		self.new_pushButton_0.setGeometry(QtCore.QRect(410, 290, 100, 100))
		self.new_pushButton_0.setStyleSheet("background-color: rgb(60, 60, 60);\n"
"color: rgb(227, 227, 227); border: 0.5px solid rgb(70, 70, 70);")
		self.new_pushButton_0.setObjectName("new_pushButton_0")
		self.new_pushButton_ok = QtWidgets.QPushButton(self.new_fingerprint_page)
		self.new_pushButton_ok.setGeometry(QtCore.QRect(510, 290, 100, 100))
		self.new_pushButton_ok.setStyleSheet("background-color: rgb(60, 60, 60);\n"
"color: rgb(227, 227, 227); border: 0.5px solid rgb(70, 70, 70);")
		self.new_pushButton_ok.setObjectName("new_pushButton_ok")
		self.new_label_text = QtWidgets.QLabel(self.new_fingerprint_page)
		self.new_label_text.setGeometry(QtCore.QRect(40, 0, 521, 160))
		self.new_label_text.setAutoFillBackground(False)
		self.new_label_text.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(30, 30, 30);   \n"
"border: 1px solid rgb(70, 70, 70);\n"
"font-size: 35px;")
		self.new_label_text.setAlignment(QtCore.Qt.AlignCenter)
		self.new_label_text.setObjectName("new_label_text")
		self.pages.addWidget(self.new_fingerprint_page)
		self.delete_fingerprint_page = QtWidgets.QWidget()
		self.delete_fingerprint_page.setObjectName("delete_fingerprint_page")
		self.delete_pushButton_1 = QtWidgets.QPushButton(self.delete_fingerprint_page)
		self.delete_pushButton_1.setGeometry(QtCore.QRect(10, 180, 100, 100))
		self.delete_pushButton_1.setStyleSheet("background-color: rgb(60, 60, 60);\n"
"color: rgb(227, 227, 227); border: 0.5px solid rgb(70, 70, 70);")
		self.delete_pushButton_1.setObjectName("delete_pushButton_1")
		self.delete_pushButton_2 = QtWidgets.QPushButton(self.delete_fingerprint_page)
		self.delete_pushButton_2.setGeometry(QtCore.QRect(110, 180, 100, 100))
		self.delete_pushButton_2.setStyleSheet("background-color: rgb(60, 60, 60);\n"
"color: rgb(227, 227, 227); border: 0.5px solid rgb(70, 70, 70);")
		self.delete_pushButton_2.setObjectName("delete_pushButton_2")
		self.delete_pushButton_3 = QtWidgets.QPushButton(self.delete_fingerprint_page)
		self.delete_pushButton_3.setGeometry(QtCore.QRect(210, 180, 100, 100))
		self.delete_pushButton_3.setStyleSheet("background-color: rgb(60, 60, 60);\n"
"color: rgb(227, 227, 227); border: 0.5px solid rgb(70, 70, 70);")
		self.delete_pushButton_3.setObjectName("delete_pushButton_3")
		self.delete_pushButton_4 = QtWidgets.QPushButton(self.delete_fingerprint_page)
		self.delete_pushButton_4.setGeometry(QtCore.QRect(310, 180, 100, 100))
		self.delete_pushButton_4.setStyleSheet("background-color: rgb(60, 60, 60);\n"
"color: rgb(227, 227, 227); border: 0.5px solid rgb(70, 70, 70);")
		self.delete_pushButton_4.setObjectName("delete_pushButton_4")
		self.delete_pushButton_5 = QtWidgets.QPushButton(self.delete_fingerprint_page)
		self.delete_pushButton_5.setGeometry(QtCore.QRect(410, 180, 100, 100))
		self.delete_pushButton_5.setStyleSheet("background-color: rgb(60, 60, 60);\n"
"color: rgb(227, 227, 227); border: 0.5px solid rgb(70, 70, 70);")
		self.delete_pushButton_5.setObjectName("delete_pushButton_5")
		self.delete_pushButton_back = QtWidgets.QPushButton(self.delete_fingerprint_page)
		self.delete_pushButton_back.setGeometry(QtCore.QRect(510, 180, 100, 100))
		self.delete_pushButton_back.setStyleSheet("background-color: rgb(60, 60, 60);\n"
"color: rgb(227, 227, 227); border: 0.5px solid rgb(70, 70, 70);")
		self.delete_pushButton_back.setObjectName("delete_pushButton_back")
		self.delete_pushButton_6 = QtWidgets.QPushButton(self.delete_fingerprint_page)
		self.delete_pushButton_6.setGeometry(QtCore.QRect(10, 290, 100, 100))
		self.delete_pushButton_6.setStyleSheet("background-color: rgb(60, 60, 60);\n"
"color: rgb(227, 227, 227); border: 0.5px solid rgb(70, 70, 70);")
		self.delete_pushButton_6.setObjectName("delete_pushButton_6")
		self.delete_pushButton_7 = QtWidgets.QPushButton(self.delete_fingerprint_page)
		self.delete_pushButton_7.setGeometry(QtCore.QRect(110, 290, 100, 100))
		self.delete_pushButton_7.setStyleSheet("background-color: rgb(60, 60, 60);\n"
"color: rgb(227, 227, 227); border: 0.5px solid rgb(70, 70, 70);")
		self.delete_pushButton_7.setObjectName("delete_pushButton_7")
		self.delete_pushButton_8 = QtWidgets.QPushButton(self.delete_fingerprint_page)
		self.delete_pushButton_8.setGeometry(QtCore.QRect(210, 290, 100, 100))
		self.delete_pushButton_8.setStyleSheet("background-color: rgb(60, 60, 60);\n"
"color: rgb(227, 227, 227); border: 0.5px solid rgb(70, 70, 70);")
		self.delete_pushButton_8.setObjectName("delete_pushButton_8")
		self.delete_pushButton_9 = QtWidgets.QPushButton(self.delete_fingerprint_page)
		self.delete_pushButton_9.setGeometry(QtCore.QRect(310, 290, 100, 100))
		self.delete_pushButton_9.setStyleSheet("background-color: rgb(60, 60, 60);\n"
"color: rgb(227, 227, 227); border: 0.5px solid rgb(70, 70, 70);")
		self.delete_pushButton_9.setObjectName("delete_pushButton_9")
		self.delete_pushButton_0 = QtWidgets.QPushButton(self.delete_fingerprint_page)
		self.delete_pushButton_0.setGeometry(QtCore.QRect(410, 290, 100, 100))
		self.delete_pushButton_0.setStyleSheet("background-color: rgb(60, 60, 60);\n"
"color: rgb(227, 227, 227); border: 0.5px solid rgb(70, 70, 70);")
		self.delete_pushButton_0.setObjectName("delete_pushButton_0")
		self.delete_pushButton_ok = QtWidgets.QPushButton(self.delete_fingerprint_page)
		self.delete_pushButton_ok.setGeometry(QtCore.QRect(510, 290, 100, 100))
		self.delete_pushButton_ok.setStyleSheet("background-color: rgb(60, 60, 60);\n"
"color: rgb(227, 227, 227); border: 0.5px solid rgb(70, 70, 70);")
		self.delete_pushButton_ok.setObjectName("delete_pushButton_ok")
		self.delete_label_text = QtWidgets.QLabel(self.delete_fingerprint_page)
		self.delete_label_text.setGeometry(QtCore.QRect(40, 0, 521, 160))
		self.delete_label_text.setAutoFillBackground(False)
		self.delete_label_text.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(30, 30, 30);   \n"
"border: 1px solid rgb(70, 70, 70);\n"
"font-size: 35px;")
		self.delete_label_text.setAlignment(QtCore.Qt.AlignCenter)
		self.delete_label_text.setObjectName("delete_label_text")
		self.pages.addWidget(self.delete_fingerprint_page)
		MainWindow.setCentralWidget(self.centralwidget)

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)
		self.button_true()

		# 세팅 완료 후 자동으로 출석 페이지 클릭
		self.fingerprint_button.click()

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
		self.fingerprint_button.setText(_translate("MainWindow", "출석"))
		self.outing_button.setText(_translate("MainWindow", "외출"))
		self.new_fingerprint_button.setText(_translate("MainWindow", "지문 등록"))
		self.delete_fingerprint_button.setText(_translate("MainWindow", "지문 삭제"))
		self.fp_label_date.setText(_translate("MainWindow", "YYYY.mm.dd 오전 HH:MM:SS"))
		self.fp_label_now.setText(_translate("MainWindow", "현재 재실: 00명"))
		self.fp_label_text.setText(_translate("MainWindow", "지문을 인식해 주세요"))
		self.fp_pushButton_on.setText(_translate("MainWindow", "등교"))
		self.fp_pushButton_out.setText(_translate("MainWindow", "하교"))
		self.out_label_date.setText(_translate("MainWindow", "YYYY.mm.dd 오전 HH:MM:SS"))
		self.out_label_now.setText(_translate("MainWindow", "현재 재실: 00명"))
		self.out_label_text.setText(_translate("MainWindow", "지문을 인식해 주세요"))
		self.out_pushButton_gohan.setText(_translate("MainWindow", "식사"))
		self.out_pushButton_lib.setText(_translate("MainWindow", "도서관"))
		self.out_pushButton_else.setText(_translate("MainWindow", "기타"))
		self.out_pushButton_return.setText(_translate("MainWindow", "복귀"))
		self.new_pushButton_1.setText(_translate("MainWindow", "1"))
		self.new_pushButton_2.setText(_translate("MainWindow", "2"))
		self.new_pushButton_3.setText(_translate("MainWindow", "3"))
		self.new_pushButton_4.setText(_translate("MainWindow", "4"))
		self.new_pushButton_5.setText(_translate("MainWindow", "5"))
		self.new_pushButton_back.setText(_translate("MainWindow", "<-"))
		self.new_pushButton_6.setText(_translate("MainWindow", "6"))
		self.new_pushButton_7.setText(_translate("MainWindow", "7"))
		self.new_pushButton_8.setText(_translate("MainWindow", "8"))
		self.new_pushButton_9.setText(_translate("MainWindow", "9"))
		self.new_pushButton_0.setText(_translate("MainWindow", "0"))
		self.new_pushButton_ok.setText(_translate("MainWindow", "확인"))
		self.new_label_text.setText(_translate("MainWindow", "학번을 입력해주세요"))
		self.delete_pushButton_1.setText(_translate("MainWindow", "1"))
		self.delete_pushButton_2.setText(_translate("MainWindow", "2"))
		self.delete_pushButton_3.setText(_translate("MainWindow", "3"))
		self.delete_pushButton_4.setText(_translate("MainWindow", "4"))
		self.delete_pushButton_5.setText(_translate("MainWindow", "5"))
		self.delete_pushButton_back.setText(_translate("MainWindow", "<-"))
		self.delete_pushButton_6.setText(_translate("MainWindow", "6"))
		self.delete_pushButton_7.setText(_translate("MainWindow", "7"))
		self.delete_pushButton_8.setText(_translate("MainWindow", "8"))
		self.delete_pushButton_9.setText(_translate("MainWindow", "9"))
		self.delete_pushButton_0.setText(_translate("MainWindow", "0"))
		self.delete_pushButton_ok.setText(_translate("MainWindow", "확인"))
		self.delete_label_text.setText(_translate("MainWindow", "학번을 입력해주세요"))
		
		self.new_pushButton_0.clicked.connect(lambda: self.changeStdNum(0))
		self.new_pushButton_1.clicked.connect(lambda: self.changeStdNum(1))
		self.new_pushButton_2.clicked.connect(lambda: self.changeStdNum(2))
		self.new_pushButton_3.clicked.connect(lambda: self.changeStdNum(3))
		self.new_pushButton_4.clicked.connect(lambda: self.changeStdNum(4))
		self.new_pushButton_5.clicked.connect(lambda: self.changeStdNum(5))
		self.new_pushButton_6.clicked.connect(lambda: self.changeStdNum(6))
		self.new_pushButton_7.clicked.connect(lambda: self.changeStdNum(7))
		self.new_pushButton_8.clicked.connect(lambda: self.changeStdNum(8))
		self.new_pushButton_9.clicked.connect(lambda: self.changeStdNum(9))
		self.new_pushButton_back.clicked.connect(lambda: self.changeStdNum("back"))

		self.delete_pushButton_0.clicked.connect(lambda: self.changeStdNum(0))
		self.delete_pushButton_1.clicked.connect(lambda: self.changeStdNum(1))
		self.delete_pushButton_2.clicked.connect(lambda: self.changeStdNum(2))
		self.delete_pushButton_3.clicked.connect(lambda: self.changeStdNum(3))
		self.delete_pushButton_4.clicked.connect(lambda: self.changeStdNum(4))
		self.delete_pushButton_5.clicked.connect(lambda: self.changeStdNum(5))
		self.delete_pushButton_6.clicked.connect(lambda: self.changeStdNum(6))
		self.delete_pushButton_7.clicked.connect(lambda: self.changeStdNum(7))
		self.delete_pushButton_8.clicked.connect(lambda: self.changeStdNum(8))
		self.delete_pushButton_9.clicked.connect(lambda: self.changeStdNum(9))
		self.delete_pushButton_back.clicked.connect(lambda: self.changeStdNum("back"))
		self.showTime()

    # 페이지 전환 함수
	def changePage(self, pageIndex):
		self.pages.setCurrentIndex(pageIndex)
		self.buttons = [self.fingerprint_button, self.outing_button, self.new_fingerprint_button, self.delete_fingerprint_button]
		for button in self.buttons:
			button.setStyleSheet("background-color: rgb(78, 78, 78); color: rgb(227, 227, 227); border: 0px;")
		self.buttons[pageIndex].setStyleSheet("background-color: gray; color: rgb(227, 227, 227); border: 0px;")
		
		# 페이지 전환 시 학번 초기화
		self.stdNum = ""
		self.new_label_text.setText("학번을 입력해주세요")
		self.delete_label_text.setText("학번을 입력해주세요")

	# 학번 입력 함수
	def changeStdNum(self, num):
		num = str(num)
		if num == "back" and self.stdNum != "":
			self.stdNum = self.stdNum[:-1]
		elif num == "back" and self.stdNum == "":
			pass
		else:
			self.stdNum += num

		self.new_label_text.setText(self.stdNum)
		self.delete_label_text.setText(self.stdNum)
		
		if self.stdNum == "":
			self.new_label_text.setText("학번을 입력해주세요")
			self.delete_label_text.setText("학번을 입력해주세요")

	def showTime(self):
		current_date = QDateTime.currentDateTime()
		current_date = current_date.toString('yyyy-MM-dd\thh:mm:ss')
		self.fp_label_date.setText(current_date)
		self.out_label_date.setText(current_date)

		timer = Timer(1, self.showTime)
		timer.start()

	# 지문 로그를 보낼 버튼이 눌렀을 때 실행되는 함수
	def log(self, action):
		self.button_false()
		
		self.activate = True
		self.start_time = time.time()
		self.action = action

		while self.activate and time.time() - self.start_time < 3:
			if f.readImage() != False:
				f.convertImage(0x01)
				print(f.searchTemplate())
				
				self.activate = False
		
		print(self.action)

		self.button_true()

	# 지문 데이터를 수정할 버튼이 눌렀을 때 실행되는 함수
	# TODO 지문 삭제 기능 추가 필요
	def data(self, action):
		self.button_false()

		# 이미 지문이 등록된 학번인지 체크
		res = requests.get(SERVER_URL + "/fingerprint/student/" + self.stdNum)

		# 등록 가능한 학번인 경우
		if res.json()["success"]:

			self.activate = True
			self.start_time = time.time()
			self.action = action

			while self.activate and time.time() - self.start_time < 3:
				if f.readImage() != False:
					f.convertImage(0x01)
					
					self.activate = False
			
			self.activate = True

			while self.activate and time.time() - self.start_time < 3:
				if f.readImage() != False:
					f.convertImage(0x02)

					salt = os.urandom(16)
					key = self.generate_key(PASSWORD, salt)

					self.fpData1 = f.downloadCharacteristics(0x01)
					self.fpData2 = f.downloadCharacteristics(0x02)

					self.fpData1 = self.encrypt(self.fpData1, key)
					self.fpData2 = self.encrypt(self.fpData2, key)

					self.fpData1 = base64.b64encode(self.fpData1)
					self.fpData2 = base64.b64encode(self.fpData2)

					self.fpData1 = self.fpData1.decode("utf-8")
					self.fpData2 = self.fpData2.decode("utf-8")

					# TODO 지문 정보 백엔드로 전송 필요
					new_fingerprint_dic["fingerprint1"] = self.fpData1
					new_fingerprint_dic["fingerprint2"] = self.fpData2
					new_fingerprint_dic["std_num"] = self.stdNum
					new_fingerprint_dic["salt"] = salt

					headers = {
						'Content-Type': 'application/json'
					}

					res = requests.post(f"{SERVER_URL}/fingerprint/students", data= json.dumps(new_fingerprint_dic), headers=headers)

					print(res.json())

					self.fpData1 = base64.b64decode(self.fpData1)
					self.fpData2 = base64.b64decode(self.fpData2)

					f.uploadCharacteristics(0x01, self.fpData1)
					f.uploadCharacteristics(0x02, self.fpData2)

					f.createTemplate()

					index = f.storeTemplate()

					print(index)

					# print(self.fpData)

					# print(type(self.fpData))
					
					self.activate = False
			
			print(self.action)

			self.button_true()
			return

		elif res.json()["success"] == False:
			self.new_label_text.setText(res.json()["message"])	# 가입 되지 않은 학번입니다.
			self.button_true()
			return
		
		else:
			self.new_label_text.setText("서버와의 연결에 문제가 있습니다.")
			self.button_true()
			return

	# 버튼 비활성화 함수
	def button_false(self):
		self.fp_pushButton_on.clicked.disconnect()
		self.fp_pushButton_out.clicked.disconnect()
		self.out_pushButton_gohan.clicked.disconnect()
		self.out_pushButton_lib.clicked.disconnect()
		self.out_pushButton_else.clicked.disconnect()
		self.out_pushButton_return.clicked.disconnect()
		self.new_pushButton_ok.clicked.disconnect()
		self.delete_pushButton_ok.clicked.disconnect()
		print("버튼 비활성화")

	# 버튼 활성화 함수
	def button_true(self):
		self.fp_pushButton_on.clicked.connect(lambda: self.log("on"))
		self.fp_pushButton_out.clicked.connect(lambda: self.log("out"))
		self.out_pushButton_gohan.clicked.connect(lambda: self.log("gohan"))
		self.out_pushButton_lib.clicked.connect(lambda: self.log("lib"))
		self.out_pushButton_else.clicked.connect(lambda: self.log("else"))
		self.out_pushButton_return.clicked.connect(lambda: self.log("return"))
		self.new_pushButton_ok.clicked.connect(lambda: self.data("ok"))
		self.delete_pushButton_ok.clicked.connect(lambda: self.data("ok"))
		print("버튼 활성화")

	
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

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
