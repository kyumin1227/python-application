from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QTime, QDateTime, Qt
from threading import Timer
from dotenv import load_dotenv
import threading
import time, json, requests, socket
import sys, os
import pygame

from pyfingerprint.pyfingerprint import PyFingerprint

# dotenv를 사용해 url주소 가져오기
load_dotenv(verbose=True)
## 1801072
URL_MAIN = os.getenv('URL_MAIN')
URL_NUMCHECK = os.getenv('URL_NUMCHECK')
URL_ENROLL = os.getenv('URL_ENROLL')
URL_DELETE = os.getenv('URL_DELETE')
URL_FINGER = os.getenv('URL_FINGER')
URL_LIMIT = os.getenv('URL_LIMIT')
URL_OUT = os.getenv('URL_OUT')
try:
    f = PyFingerprint('/dev/ttyAMA0', 57600, 0xFFFFFFFF, 0x00000000)
    ## BaudRate, ## address , ## password
except Exception as e:
    print('센서 정보를 확인할 수 없습니다!')
    exit(1)
def get_Finger_List():
    response = requests.post(URL_FINGER)
    finger_list = json.loads(response.text)
    #f.clearDatabase()
    for i in range(0, len(finger_list)):
        #f.deleteTemplate(i)
        #f.uploadCharacteristics(0x01, eval(finger_list[i]['serial_num']))
        #f.createTemplate()
        #positionNumber = f.storeTemplate()
        Std_DATA[i] = finger_list[i]['std_num']

Main_ID ={
    "primaryKEY" : '1601136',
    "tab" : 'false'
}

Main_CHECK = {
    "userName" : 'NULL',
    "data" : 'true',
    "check" : 'NULL'
}

Enroll_NAME = {
    "std_num" : ''
}

Enroll_FLAG = {
    "enroll_flag" : 'false',
    "flag_exist": 'false',  # 입력한 학번 존재 유무 확인 값
    "userName": 'NULL'
}

Enroll_ID = {
    "userID": 'NULL',       # 사용자 이름
    "primaryKEY": 'NULL',   # 사용자 지문 번호
}

Delete_ID = {
    "primaryKEY" : '1801072'
}

Outgo_ID = {
    "primaryKEY" : '1601136',
    "reason" : '식사'
}

Outgo_FLAG = {
        "std_name" : "null",
        "in_time" : "null",
        "out_time" : "null",
        "reason" : "null",
        "outgoing_time":"null"
    }

Std_DATA = {

}

#response = requests.post(URL_MAIN, data=Main_ID)
#print(json.loads(response.text))

response = requests.post(URL_DELETE, data=Delete_ID)
Main_CHECK = json.loads(response.text)
get_Finger_List()
print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))
print(Std_DATA)
#f.clearDatabase()
