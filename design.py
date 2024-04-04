# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './fingerPrint/fingerPrint_kyumin/qt-designer/ammend_2.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(811, 480)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.fingerprint_button = QtWidgets.QPushButton(self.centralwidget)
        self.fingerprint_button.setGeometry(QtCore.QRect(40, 40, 131, 101))
        self.fingerprint_button.setObjectName("fingerprint_button")
        self.fingerprint_button.clicked.connect(lambda: self.changePage(0))
        self.outing_button = QtWidgets.QPushButton(self.centralwidget)
        self.outing_button.setGeometry(QtCore.QRect(40, 140, 131, 101))
        self.outing_button.setObjectName("outing_button")
        self.outing_button.clicked.connect(lambda: self.changePage(1))
        self.new_fingerprint_button = QtWidgets.QPushButton(self.centralwidget)
        self.new_fingerprint_button.setGeometry(QtCore.QRect(40, 240, 131, 101))
        self.new_fingerprint_button.setObjectName("new_fingerprint_button")
        self.new_fingerprint_button.clicked.connect(lambda: self.changePage(2))
        self.delete_fingerprint_button = QtWidgets.QPushButton(self.centralwidget)
        self.delete_fingerprint_button.setGeometry(QtCore.QRect(40, 340, 131, 101))
        self.delete_fingerprint_button.setObjectName("delete_fingerprint_button")
        self.delete_fingerprint_button.clicked.connect(lambda: self.changePage(3))
        self.pages = QtWidgets.QStackedWidget(self.centralwidget)
        self.pages.setGeometry(QtCore.QRect(180, 40, 611, 391))
        self.pages.setObjectName("pages")
        self.fingerprint_page = QtWidgets.QWidget()
        self.fingerprint_page.setObjectName("fingerprint_page")
        self.radioButton_going = QtWidgets.QRadioButton(self.fingerprint_page)
        self.radioButton_going.setGeometry(QtCore.QRect(160, 170, 100, 20))
        self.radioButton_going.setObjectName("radioButton_going")
        self.radioButton_leaving = QtWidgets.QRadioButton(self.fingerprint_page)
        self.radioButton_leaving.setGeometry(QtCore.QRect(380, 170, 100, 20))
        self.radioButton_leaving.setObjectName("radioButton_leaving")
        self.textBrowser = QtWidgets.QTextBrowser(self.fingerprint_page)
        self.textBrowser.setGeometry(QtCore.QRect(70, 230, 471, 41))
        self.textBrowser.setObjectName("textBrowser")
        self.textEdit = QtWidgets.QTextEdit(self.fingerprint_page)
        self.textEdit.setGeometry(QtCore.QRect(100, 290, 421, 79))
        self.textEdit.setObjectName("textEdit")
        self.textEdit_date = QtWidgets.QTextEdit(self.fingerprint_page)
        self.textEdit_date.setGeometry(QtCore.QRect(40, 30, 520, 101))
        self.textEdit_date.setObjectName("textEdit_date")
        self.pages.addWidget(self.fingerprint_page)
        self.outing_page = QtWidgets.QWidget()
        self.outing_page.setObjectName("outing_page")
        self.radioButton_food = QtWidgets.QRadioButton(self.outing_page)
        self.radioButton_food.setGeometry(QtCore.QRect(120, 170, 100, 20))
        self.radioButton_food.setObjectName("radioButton_food")
        self.radioButton_lib = QtWidgets.QRadioButton(self.outing_page)
        self.radioButton_lib.setGeometry(QtCore.QRect(270, 170, 100, 20))
        self.radioButton_lib.setObjectName("radioButton_lib")
        self.radioButton_else = QtWidgets.QRadioButton(self.outing_page)
        self.radioButton_else.setGeometry(QtCore.QRect(420, 170, 100, 20))
        self.radioButton_else.setObjectName("radioButton_else")
        self.textBrowser_outing = QtWidgets.QTextBrowser(self.outing_page)
        self.textBrowser_outing.setGeometry(QtCore.QRect(70, 230, 471, 41))
        self.textBrowser_outing.setObjectName("textBrowser_outing")
        self.textEdit_outing = QtWidgets.QTextEdit(self.outing_page)
        self.textEdit_outing.setGeometry(QtCore.QRect(100, 290, 421, 79))
        self.textEdit_outing.setObjectName("textEdit_outing")
        self.textEdit_date_outing = QtWidgets.QTextEdit(self.outing_page)
        self.textEdit_date_outing.setGeometry(QtCore.QRect(40, 30, 520, 101))
        self.textEdit_date_outing.setObjectName("textEdit_date_outing")
        self.pages.addWidget(self.outing_page)
        self.new_fingerprint_page = QtWidgets.QWidget()
        self.new_fingerprint_page.setObjectName("new_fingerprint_page")
        self.textEdit_new = QtWidgets.QTextEdit(self.new_fingerprint_page)
        self.textEdit_new.setGeometry(QtCore.QRect(100, 50, 421, 79))
        self.textEdit_new.setObjectName("textEdit_new")
        self.pushButton_1_new = QtWidgets.QPushButton(self.new_fingerprint_page)
        self.pushButton_1_new.setGeometry(QtCore.QRect(10, 170, 100, 100))
        self.pushButton_1_new.setObjectName("pushButton_1_new")
        self.pushButton_2_new = QtWidgets.QPushButton(self.new_fingerprint_page)
        self.pushButton_2_new.setGeometry(QtCore.QRect(110, 170, 100, 100))
        self.pushButton_2_new.setObjectName("pushButton_2_new")
        self.pushButton_3_new = QtWidgets.QPushButton(self.new_fingerprint_page)
        self.pushButton_3_new.setGeometry(QtCore.QRect(210, 170, 100, 100))
        self.pushButton_3_new.setObjectName("pushButton_3_new")
        self.pushButton_4_new = QtWidgets.QPushButton(self.new_fingerprint_page)
        self.pushButton_4_new.setGeometry(QtCore.QRect(310, 170, 100, 100))
        self.pushButton_4_new.setObjectName("pushButton_4_new")
        self.pushButton_5_new = QtWidgets.QPushButton(self.new_fingerprint_page)
        self.pushButton_5_new.setGeometry(QtCore.QRect(410, 170, 100, 100))
        self.pushButton_5_new.setObjectName("pushButton_5_new")
        self.pushButton_back_new = QtWidgets.QPushButton(self.new_fingerprint_page)
        self.pushButton_back_new.setGeometry(QtCore.QRect(510, 170, 100, 100))
        self.pushButton_back_new.setObjectName("pushButton_back_new")
        self.pushButton_6_new = QtWidgets.QPushButton(self.new_fingerprint_page)
        self.pushButton_6_new.setGeometry(QtCore.QRect(10, 280, 100, 100))
        self.pushButton_6_new.setObjectName("pushButton_6_new")
        self.pushButton_7_new = QtWidgets.QPushButton(self.new_fingerprint_page)
        self.pushButton_7_new.setGeometry(QtCore.QRect(110, 280, 100, 100))
        self.pushButton_7_new.setObjectName("pushButton_7_new")
        self.pushButton_8_new = QtWidgets.QPushButton(self.new_fingerprint_page)
        self.pushButton_8_new.setGeometry(QtCore.QRect(210, 280, 100, 100))
        self.pushButton_8_new.setObjectName("pushButton_8_new")
        self.pushButton_9_new = QtWidgets.QPushButton(self.new_fingerprint_page)
        self.pushButton_9_new.setGeometry(QtCore.QRect(310, 280, 100, 100))
        self.pushButton_9_new.setObjectName("pushButton_9_new")
        self.pushButton_0_new = QtWidgets.QPushButton(self.new_fingerprint_page)
        self.pushButton_0_new.setGeometry(QtCore.QRect(410, 280, 100, 100))
        self.pushButton_0_new.setObjectName("pushButton_0_new")
        self.pushButton_check_1_new = QtWidgets.QPushButton(self.new_fingerprint_page)
        self.pushButton_check_1_new.setGeometry(QtCore.QRect(510, 280, 100, 100))
        self.pushButton_check_1_new.setObjectName("pushButton_check_1_new")
        self.pages.addWidget(self.new_fingerprint_page)
        self.delete_fingerprint_page = QtWidgets.QWidget()
        self.delete_fingerprint_page.setObjectName("delete_fingerprint_page")
        self.textEdit_delete = QtWidgets.QTextEdit(self.delete_fingerprint_page)
        self.textEdit_delete.setGeometry(QtCore.QRect(100, 50, 421, 79))
        self.textEdit_delete.setObjectName("textEdit_delete")
        self.pushButton_1_delete = QtWidgets.QPushButton(self.delete_fingerprint_page)
        self.pushButton_1_delete.setGeometry(QtCore.QRect(10, 170, 100, 100))
        self.pushButton_1_delete.setObjectName("pushButton_1_delete")
        self.pushButton_2_delete = QtWidgets.QPushButton(self.delete_fingerprint_page)
        self.pushButton_2_delete.setGeometry(QtCore.QRect(110, 170, 100, 100))
        self.pushButton_2_delete.setObjectName("pushButton_2_delete")
        self.pushButton_3_delete = QtWidgets.QPushButton(self.delete_fingerprint_page)
        self.pushButton_3_delete.setGeometry(QtCore.QRect(210, 170, 100, 100))
        self.pushButton_3_delete.setObjectName("pushButton_3_delete")
        self.pushButton_4_delete = QtWidgets.QPushButton(self.delete_fingerprint_page)
        self.pushButton_4_delete.setGeometry(QtCore.QRect(310, 170, 100, 100))
        self.pushButton_4_delete.setObjectName("pushButton_4_delete")
        self.pushButton_5_delete = QtWidgets.QPushButton(self.delete_fingerprint_page)
        self.pushButton_5_delete.setGeometry(QtCore.QRect(410, 170, 100, 100))
        self.pushButton_5_delete.setObjectName("pushButton_5_delete")
        self.pushButton_back_delete = QtWidgets.QPushButton(self.delete_fingerprint_page)
        self.pushButton_back_delete.setGeometry(QtCore.QRect(510, 170, 100, 100))
        self.pushButton_back_delete.setObjectName("pushButton_back_delete")
        self.pushButton_6_delete = QtWidgets.QPushButton(self.delete_fingerprint_page)
        self.pushButton_6_delete.setGeometry(QtCore.QRect(10, 280, 100, 100))
        self.pushButton_6_delete.setObjectName("pushButton_6_delete")
        self.pushButton_7_delete = QtWidgets.QPushButton(self.delete_fingerprint_page)
        self.pushButton_7_delete.setGeometry(QtCore.QRect(110, 280, 100, 100))
        self.pushButton_7_delete.setObjectName("pushButton_7_delete")
        self.pushButton_8_delete = QtWidgets.QPushButton(self.delete_fingerprint_page)
        self.pushButton_8_delete.setGeometry(QtCore.QRect(210, 280, 100, 100))
        self.pushButton_8_delete.setObjectName("pushButton_8_delete")
        self.pushButton_9_delete = QtWidgets.QPushButton(self.delete_fingerprint_page)
        self.pushButton_9_delete.setGeometry(QtCore.QRect(310, 280, 100, 100))
        self.pushButton_9_delete.setObjectName("pushButton_9_delete")
        self.pushButton_0_delete = QtWidgets.QPushButton(self.delete_fingerprint_page)
        self.pushButton_0_delete.setGeometry(QtCore.QRect(410, 280, 100, 100))
        self.pushButton_0_delete.setObjectName("pushButton_0_delete")
        self.pushButton_check_delete = QtWidgets.QPushButton(self.delete_fingerprint_page)
        self.pushButton_check_delete.setGeometry(QtCore.QRect(510, 280, 100, 100))
        self.pushButton_check_delete.setObjectName("pushButton_check_delete")
        self.pages.addWidget(self.delete_fingerprint_page)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.pages.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.fingerprint_button.setText(_translate("MainWindow", "출석"))
        self.outing_button.setText(_translate("MainWindow", "외출"))
        self.new_fingerprint_button.setText(_translate("MainWindow", "지문 등록"))
        self.delete_fingerprint_button.setText(_translate("MainWindow", "지문 삭제"))
        self.radioButton_going.setText(_translate("MainWindow", "등교"))
        self.radioButton_leaving.setText(_translate("MainWindow", "하교"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'.AppleSystemUIFont\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:24pt;\">지문을 인식해 주세요</span></p></body></html>"))
        self.radioButton_food.setText(_translate("MainWindow", "식사 "))
        self.radioButton_lib.setText(_translate("MainWindow", "도서관"))
        self.radioButton_else.setText(_translate("MainWindow", "기타"))
        self.textBrowser_outing.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'.AppleSystemUIFont\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:24pt;\">지문을 인식해 주세요</span></p></body></html>"))
        self.textEdit_new.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'.AppleSystemUIFont\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:24pt;\">학번을 입력해주세요</span></p></body></html>"))
        self.pushButton_1_new.setText(_translate("MainWindow", "1"))
        self.pushButton_2_new.setText(_translate("MainWindow", "2"))
        self.pushButton_3_new.setText(_translate("MainWindow", "3"))
        self.pushButton_4_new.setText(_translate("MainWindow", "4"))
        self.pushButton_5_new.setText(_translate("MainWindow", "5"))
        self.pushButton_back_new.setText(_translate("MainWindow", "<-"))
        self.pushButton_6_new.setText(_translate("MainWindow", "6"))
        self.pushButton_7_new.setText(_translate("MainWindow", "7"))
        self.pushButton_8_new.setText(_translate("MainWindow", "8"))
        self.pushButton_9_new.setText(_translate("MainWindow", "9"))
        self.pushButton_0_new.setText(_translate("MainWindow", "0"))
        self.pushButton_check_1_new.setText(_translate("MainWindow", "확인"))
        self.textEdit_delete.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'.AppleSystemUIFont\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:24pt;\">학번을 입력해주세요</span></p></body></html>"))
        self.pushButton_1_delete.setText(_translate("MainWindow", "1"))
        self.pushButton_2_delete.setText(_translate("MainWindow", "2"))
        self.pushButton_3_delete.setText(_translate("MainWindow", "3"))
        self.pushButton_4_delete.setText(_translate("MainWindow", "4"))
        self.pushButton_5_delete.setText(_translate("MainWindow", "5"))
        self.pushButton_back_delete.setText(_translate("MainWindow", "<-"))
        self.pushButton_6_delete.setText(_translate("MainWindow", "6"))
        self.pushButton_7_delete.setText(_translate("MainWindow", "7"))
        self.pushButton_8_delete.setText(_translate("MainWindow", "8"))
        self.pushButton_9_delete.setText(_translate("MainWindow", "9"))
        self.pushButton_0_delete.setText(_translate("MainWindow", "0"))
        self.pushButton_check_delete.setText(_translate("MainWindow", "확인"))


    def changePage(self, pageIndex):
        self.pages.setCurrentIndex(pageIndex)
        self.buttons = [self.fingerprint_button, self.outing_button, self.new_fingerprint_button, self.delete_fingerprint_button]
        for button in self.buttons:
            button.setStyleSheet("background-color: lightgray;")
        self.buttons[pageIndex].setStyleSheet("background-color: gray;")
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
