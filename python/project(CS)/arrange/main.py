import sys, os
from PyQt5 import QtCore, QtGui, QtWidgets
from UI import Ui_MainWindow, Analysis
from multiprocessing import Process
from threading import Thread

def Analysis_thread(ui):
    t = Thread(target = ui.Analysis, args = (ui.path_lineEdit.text(), float(ui.length_lineEdit.text(),)))
    t.start()

def Analysis_process(ui):
    p = Process(target = Analysis, args = (ui.path_lineEdit.text(), float(ui.length_lineEdit.text()), ui,))
    p.start()

def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    #ui.analysis.clicked.connect(lambda:ui.Analysis(ui.path_lineEdit.text(), float(ui.length_lineEdit.text()), ui))
    ui.analysis.clicked.connect(lambda:Analysis_thread(ui))
    #ui.analysis.clicked.connect(lambda:Analysis_process(ui))
    ui.clean.clicked.connect(ui.Clean)
    ui.close.clicked.connect(ui.Close)
    sys.exit(app.exec_())

main()