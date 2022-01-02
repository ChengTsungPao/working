from Data_Evaluation import evaluation
from Data_Training import data_training
import cv2
import numpy as np

class show_result(data_training):

    def __init__(self, path):
        super().__init__(path)

        self.predict_all_bounding_box_wider_data()
        self.predict_all_bounding_box_narrow_data()
        self.predict_all_classifier_data()

        # index = 0
        # while index < 240:
        #     self.predict_bounding_box_wider_data(index)
        #     index += 1

        # index = 0
        # while index < 120:
        #     self.predict_bounding_box_narrow_data(index)
        #     index += 1

        # index = 0
        # while index < 240:
        #     self.predict_classifier_data(index)
        #     index += 1

        self.all_bounding_box_wider_data_evaluation = []
        self.all_bounding_box_narrow_data_evaluation = []
        self.bounding_box_wider_data_evaluation()
        self.bounding_box_narrow_data_evaluation()

    
    def bounding_box_wider_data_evaluation(self):
        if self.bounding_box_wider_data == []:
            self.get_bounding_box_wider_data()

        result = np.load("./predict/bounding_box_wider_data_predict.npz")

        for index in range(len(self.bounding_box_wider_data)):

            target = self.bounding_box_wider_target[index]

            x1, y1, x2, y2 = result["predict"][index]
            predict = np.array([[x1, y1], [x1, y2], [x2, y2], [x2, y1]])

            x1, y1, x2, y2 = target
            groundTruth = np.array([[x1, y1], [x1, y2], [x2, y2], [x2, y1]])

            self.all_bounding_box_wider_data_evaluation.append(evaluation(predict, groundTruth))


    def bounding_box_narrow_data_evaluation(self):
        if self.bounding_box_narrow_data == []:
            self.get_bounding_box_narrow_data()

        result = np.load("./predict/bounding_box_narrow_data_predict.npz", allow_pickle = True)

        for index in range(len(self.bounding_box_narrow_data)):

            target =  self.bounding_box_narrow_target[index]

            predictPoints = result["predict"][index]

            x, y, width, height, angle = np.array(target, float)
            rect = (x, y), (width, height), angle
            groundTruthPoints = np.array(cv2.boxPoints(rect), int)

            self.all_bounding_box_narrow_data_evaluation.append(evaluation(predictPoints, groundTruthPoints))





