from Data_Evaluation import evaluationIOU, evaluationF1
from Data_Training import data_training
import cv2
import numpy as np

class show_result(data_training):

    def __init__(self, path):
        super().__init__(path)

        self.predict_all_bounding_box_wider_data()
        self.predict_all_bounding_box_narrow_data()
        self.predict_all_classifier_data()

        self.all_bounding_box_wider_data_evaluation = []
        self.all_bounding_box_narrow_data_evaluation = []
        self.all_classifier_data_evaluation = []
        self.classifier_data_evaluation()
        self.bounding_box_wider_data_evaluation()
        self.bounding_box_narrow_data_evaluation()

    
    def bounding_box_wider_data_evaluation(self):

        result = np.load("./predict/bounding_box_wider_data_predict.npz")

        for index in range(len(result["predict"])):

            target = result["goundTruth"][index]

            x1, y1, x2, y2 = result["predict"][index]
            predict = np.array([[x1, y1], [x1, y2], [x2, y2], [x2, y1]])

            x1, y1, x2, y2 = target
            groundTruth = np.array([[x1, y1], [x1, y2], [x2, y2], [x2, y1]])

            self.all_bounding_box_wider_data_evaluation.append(evaluationIOU(predict, groundTruth))


    def bounding_box_narrow_data_evaluation(self):

        result = np.load("./predict/bounding_box_narrow_data_predict.npz", allow_pickle = True)

        for index in range(len(result["predict"])):

            target =  result["goundTruth"][index]

            predictPoints = result["predict"][index]

            x, y, width, height, angle = np.array(target, float)
            rect = (x, y), (width, height), angle
            groundTruthPoints = np.array(cv2.boxPoints(rect), int)

            self.all_bounding_box_narrow_data_evaluation.append(evaluationIOU(predictPoints, groundTruthPoints))


    def classifier_data_evaluation(self):
        self.all_classifier_data_evaluation = evaluationF1()
        





