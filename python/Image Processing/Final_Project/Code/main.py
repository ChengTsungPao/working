from Show_Result import show_result
import numpy as np
import sys
from PyQt5 import QtWidgets
from UI import UI

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    ui = UI()
    sys.exit(app.exec_())

    # path = "./Scaphoid/"
    # show_result_fcn = show_result(path)
    # show_result_fcn.train_bounding_box_narrow_data
