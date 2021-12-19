import os
import cv2
import json
import numpy as np
import pandas as pd

class data_reader():

    def __init__(self, path):

        self.fracture_image = [] 
        self.normal_image = []
        self.fracture_filename = [] 
        self.normal_filename = []

        self.bounding_box_wider_data = []
        self.bounding_box_wider_target = []

        self.bounding_box_narrow_data = []
        self.bounding_box_narrow_target = []

        self.classifier_data = []
        self.classifier_target = []

        self.path = None

        self.setup(path)


    def setup(self, path):
        self.setPath(path)
        self.read_image()


    def setPath(self, path):
        self.path = path


    def read_data(self):
        self.get_bounding_box_wider_data()
        self.get_bounding_box_narrow_data()
        self.get_classifier_data()


    def read_image(self):
        path_image = self.path + "Images/"
        self.fracture_filename = os.listdir(path_image + "Fracture/")
        self.normal_filename = os.listdir(path_image + "Normal/")

        for filename in self.fracture_filename:
            # image = np.array(cv2.imread(path_image + "Fracture/" + filename)).astype(np.float64)
            image = np.array(cv2.imread(path_image + "Fracture/" + filename))
            self.fracture_image.append(image)

        for filename in self.normal_filename:
            # image = np.array(cv2.imread(path_image + "Normal/" + filename)).astype(np.float64)
            image = np.array(cv2.imread(path_image + "Normal/" + filename))
            self.normal_image.append(image)


    def get_bounding_box_wider_data(self):
        path_target = self.path + "Annotations/" + "Scaphoid_Slice/"

        self.bounding_box_wider_data = self.fracture_image + self.normal_image

        for filename in self.fracture_filename + self.normal_filename:
            filename = filename.split(".bmp")[0] + ".json"
            f = open(path_target + filename, "r")
            data = json.load(f)
            self.bounding_box_wider_target.append([int(position) for position in data[0]["bbox"]])


    def get_bounding_box_narrow_data(self):
        path_target = self.path + "Annotations/" + "Fracture_Coordinate/"

        self.bounding_box_narrow_data = self.fracture_image

        for filename in self.fracture_filename:
            filename = filename.split(".bmp")[0] + ".csv"
            data = pd.read_csv(path_target + filename)
            self.bounding_box_narrow_target.append(np.array([int(data[key][0]) for key in data.keys()]))


    def get_classifier_data(self):

        for image in self.fracture_image:
            self.classifier_data.append(image)
            self.classifier_target.append(0)

        for image in self.normal_image:
            self.classifier_data.append(image)
            self.classifier_target.append(1)
