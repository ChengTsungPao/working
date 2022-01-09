from PyQt5 import QtWidgets, uic
from Config import imageTempFolder, wider_data_image_filename, wider_data_result_filename, narrow_data_image_filename, narrow_data_result_filename, grad_cam_result_filename
from Show_Result import show_result
from PyQt5.QtGui import QPixmap
import numpy as np
import os

class UI(QtWidgets.QMainWindow):

    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi('UI.ui', self)

        self.path = None
        self.show_result_fcn = None
        self.imageNameTable = {}
        self.loadFolderButton.clicked.connect(self.load_folder)
        self.comboBox.currentTextChanged.connect(self.combobox_changed)
        self.show()


    def load_folder(self):
        folderpath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folderpath != "":
            self.path = folderpath + "/"
            try:
                self.setup()
                os.system("cls||clear")
                print("Complete Setup !!!")
            except:
                print("Wrong Folder !!!")


    def setup(self):
        self.show_result_fcn = show_result(self.path)

        IOU = np.mean(self.show_result_fcn.all_bounding_box_wider_data_evaluation)
        self.allDetectScaphoidLabel.setText("Detect scaphoid: IOU = {:.2f}".format(IOU))

        IOU = np.mean(self.show_result_fcn.all_bounding_box_narrow_data_evaluation)
        self.allLocationFractureLabel.setText("Location of fracture: IOU = {:.2f}".format(IOU))

        precision, recall, f1_score, accuracy = self.show_result_fcn.all_classifier_data_evaluation
        self.allClassificationLabel.setText("Classification: precision = {:.2f}  recall = {:.2f}  f1_score = {:.2f}  accuracy = {:.2f}".format(precision, recall, f1_score, accuracy))

        self.comboBox.clear()
        for i in range(len(self.show_result_fcn.fracture_filename)):
            comboBoxName = self.show_result_fcn.fracture_filename[i] + " (fracture)"
            self.imageNameTable[comboBoxName] = (i, "fracture")
            self.comboBox.addItem(comboBoxName)
        for j in range(len(self.show_result_fcn.normal_filename)):
            comboBoxName = self.show_result_fcn.normal_filename[j] + " (normal)"
            self.imageNameTable[comboBoxName] = (i + j, "normal")
            self.comboBox.addItem(comboBoxName)

        if not os.path.exists("./result/"):
            os.makedirs("./result/")

        self.originImageLabel.setScaledContents(True)
        self.detectImageLabel.setScaledContents(True)
        self.cropImageLabel.setScaledContents(True)
        self.resultImageLabel.setScaledContents(True)
        self.gradCamImageLabel.setScaledContents(True)


    def combobox_changed(self, imageName):
        if imageName == "":
            return

        index, imageType = self.imageNameTable[imageName]

        IOU = self.show_result_fcn.all_bounding_box_wider_data_evaluation[index]
        self.detectScaphoidLabel.setText("Detect scaphoid: IOU = {:.2f}".format(IOU))
        self.show_result_fcn.predict_bounding_box_wider_data(index)
        self.originImageLabel.setPixmap(QPixmap(imageTempFolder + wider_data_image_filename))
        self.detectImageLabel.setPixmap(QPixmap(imageTempFolder + wider_data_result_filename))
        self.cropImageLabel.setPixmap(QPixmap(imageTempFolder + narrow_data_image_filename))

        predict, goundTruth = self.show_result_fcn.predict_classifier_data(index)
        self.typeLabel.setText("Type: {}".format(goundTruth))
        self.predictLabel.setText("Predict: {}".format(predict))
        self.gradCamImageLabel.setPixmap(QPixmap(imageTempFolder + grad_cam_result_filename))

        if imageType == "fracture":
            IOU = self.show_result_fcn.all_bounding_box_narrow_data_evaluation[index]
            self.locationFractureLabel.setText("Location of fracture: IOU = {:.2f}".format(IOU))
            self.show_result_fcn.predict_bounding_box_narrow_data(index)
            self.resultImageLabel.setPixmap(QPixmap(imageTempFolder + narrow_data_result_filename))

        else:
            self.locationFractureLabel.setText("Location of fracture: XX")
            self.resultImageLabel.clear()


    