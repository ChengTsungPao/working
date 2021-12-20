from PCA import pca

from PyQt5 import QtWidgets, uic


class UI(QtWidgets.QMainWindow):

    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi('UI.ui', self)

        # Image and Library Path
        self.path = ".//Dataset_CvDl_Hw2//Q{}_Image//"

        # problem = 4 UI connect
        self.pca_fcn = None
        self.Image_Reconstruction.clicked.connect(self.image_reconstruction)
        self.Reconstruction_Error.clicked.connect(self.reconstruction_error)

        self.show()

    # setup function
    def setup_pca(self):
        self.pca_fcn = pca(self.path.format(4))

    # problem 4
    def image_reconstruction(self):
        if self.pca_fcn == None:
            self.setup_pca()

        self.pca_fcn.image_reconstruction()

    def reconstruction_error(self):
        if self.pca_fcn == None:
            self.setup_pca()

        self.pca_fcn.compute_reconstruction_error()