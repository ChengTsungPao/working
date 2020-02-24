# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

var=1
cluster="good"

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(876, 676)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.output = QtWidgets.QPushButton(self.centralwidget)
        self.output.setGeometry(QtCore.QRect(620, 480, 91, 31))
        self.output.setObjectName("output")
        self.next = QtWidgets.QPushButton(self.centralwidget)
        self.next.setGeometry(QtCore.QRect(440, 580, 91, 31))
        self.next.setStyleSheet("")
        self.next.setAutoDefault(False)
        self.next.setFlat(False)
        self.next.setObjectName("next")
        self.back = QtWidgets.QPushButton(self.centralwidget)
        self.back.setGeometry(QtCore.QRect(40, 580, 91, 31))
        self.back.setObjectName("back")
        self.in_rad = QtWidgets.QLabel(self.centralwidget)
        self.in_rad.setGeometry(QtCore.QRect(570, 97, 51, 41))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        self.in_rad.setFont(font)
        self.in_rad.setObjectName("in_rad")
        self.out_rad = QtWidgets.QLabel(self.centralwidget)
        self.out_rad.setGeometry(QtCore.QRect(570, 147, 51, 41))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        self.out_rad.setFont(font)
        self.out_rad.setObjectName("out_rad")
        self.area = QtWidgets.QLabel(self.centralwidget)
        self.area.setGeometry(QtCore.QRect(570, 197, 51, 41))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        self.area.setFont(font)
        self.area.setObjectName("area")
        self.out_rad_val = QtWidgets.QLabel(self.centralwidget)
        self.out_rad_val.setGeometry(QtCore.QRect(640, 150, 51, 41))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        self.out_rad_val.setFont(font)
        self.out_rad_val.setObjectName("out_rad_val")
        self.area_val = QtWidgets.QLabel(self.centralwidget)
        self.area_val.setGeometry(QtCore.QRect(640, 200, 51, 41))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        self.area_val.setFont(font)
        self.area_val.setObjectName("area_val")
        self.in_rad_val = QtWidgets.QLabel(self.centralwidget)
        self.in_rad_val.setGeometry(QtCore.QRect(640, 100, 51, 41))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        self.in_rad_val.setFont(font)
        self.in_rad_val.setObjectName("in_rad_val")
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(570, 290, 121, 19))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_2.setGeometry(QtCore.QRect(570, 320, 121, 19))
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_3 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_3.setGeometry(QtCore.QRect(570, 380, 151, 19))
        self.radioButton_3.setObjectName("radioButton_3")
        self.radioButton_4 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_4.setGeometry(QtCore.QRect(570, 350, 131, 19))
        self.radioButton_4.setObjectName("radioButton_4")
        self.radioButton_5 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_5.setGeometry(QtCore.QRect(570, 410, 98, 19))
        self.radioButton_5.setObjectName("radioButton_5")
        self.photo = QtWidgets.QLabel(self.centralwidget)
        self.photo.setGeometry(QtCore.QRect(40, 30, 561, 541))
        self.photo.setText("")
        self.photo.setPixmap(QtGui.QPixmap("good1.bmp"))
        self.photo.setObjectName("photo")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 876, 31))
        self.menubar.setObjectName("menubar")
        self.menufile = QtWidgets.QMenu(self.menubar)
        self.menufile.setEnabled(True)
        self.menufile.setGeometry(QtCore.QRect(2263, 206, 187, 161))
        self.menufile.setObjectName("menufile")
        self.menuedit = QtWidgets.QMenu(self.menubar)
        self.menuedit.setObjectName("menuedit")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.openfile = QtWidgets.QAction(MainWindow)
        self.openfile.setObjectName("openfile")
        self.save = QtWidgets.QAction(MainWindow)
        self.save.setObjectName("save")
        self.save_as = QtWidgets.QAction(MainWindow)
        self.save_as.setObjectName("save_as")
        self.setting = QtWidgets.QAction(MainWindow)
        self.setting.setObjectName("setting")
        self.menufile.addAction(self.openfile)
        self.menufile.addAction(self.save)
        self.menufile.addAction(self.save_as)
        self.menuedit.addAction(self.setting)
        self.menubar.addAction(self.menufile.menuAction())
        self.menubar.addAction(self.menuedit.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        self.next.clicked.connect(self.next_picture)
        self.back.clicked.connect(self.back_picture)
        self.radioButton_2.clicked.connect(self.good_pictures)
        self.radioButton_3.clicked.connect(self.bad_pictures)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.output.setText(_translate("MainWindow", "output"))
        self.next.setText(_translate("MainWindow", "next"))
        self.back.setText(_translate("MainWindow", "back"))
        self.in_rad.setText(_translate("MainWindow", "內徑"))
        self.out_rad.setText(_translate("MainWindow", "外徑"))
        self.area.setText(_translate("MainWindow", "面積"))
        self.out_rad_val.setText(_translate("MainWindow", "??"))
        self.area_val.setText(_translate("MainWindow", "??"))
        self.in_rad_val.setText(_translate("MainWindow", "??"))
        self.radioButton.setText(_translate("MainWindow", "多顆健康血球"))
        self.radioButton_2.setText(_translate("MainWindow", "單顆健康血球"))
        self.radioButton_3.setText(_translate("MainWindow", "單顆不健康血球"))
        self.radioButton_4.setText(_translate("MainWindow", "多顆不健康血球"))
        self.radioButton_5.setText(_translate("MainWindow", "全部血球"))
        self.menufile.setTitle(_translate("MainWindow", "file"))
        self.menuedit.setTitle(_translate("MainWindow", "edit"))
        self.openfile.setText(_translate("MainWindow", "open file"))
        self.save.setText(_translate("MainWindow", "save"))
        self.save_as.setText(_translate("MainWindow", "save as"))
        self.setting.setText(_translate("MainWindow", "setting"))
    
    def next_picture(self):
        global var
        global cluster
        if var<11:
            self.photo.setPixmap(QtGui.QPixmap(cluster+str(var)+".bmp"))
            var+=1
    
    def back_picture(self):
        global var
        global cluster
        if var>1:
            self.photo.setPixmap(QtGui.QPixmap(cluster+str(var)+".bmp"))
            var-=1
    
    def good_pictures(self):
        global var
        global cluster
        var=1
        cluster="good"
        self.photo.setPixmap(QtGui.QPixmap(cluster+str(var)+".bmp"))
    
    def bad_pictures(self):
        global var
        global cluster
        var=1
        cluster="bad"
        self.photo.setPixmap(QtGui.QPixmap(cluster+str(var)+".bmp"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

