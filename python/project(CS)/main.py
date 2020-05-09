import sys, os
from PyQt5 import QtCore, QtGui, QtWidgets
from UI import Ui_MainWindow
from threading import Thread
import warnings
warnings.filterwarnings("ignore")

def Analysis_thread(ui):
    t = Thread(target = ui.Analysis, args = (ui.path_lineEdit.text(), ui.length_lineEdit.text(),))
    t.start()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    #ui.analysis.clicked.connect(lambda:ui.Analysis(ui.path_lineEdit.text(), ui.length_lineEdit.text()))
    ui.analysis.clicked.connect(lambda:Analysis_thread(ui))
    ui.clean.clicked.connect(ui.Clean)
    ui.close.clicked.connect(ui.Close)
    sys.exit(app.exec_())
