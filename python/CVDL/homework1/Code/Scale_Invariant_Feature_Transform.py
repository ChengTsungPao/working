import cv2
import numpy as np
import matplotlib.pylab as plt

class scale_invariant_feature_transform():

    def __init__(self, path):
        self.path = path

        self.image1 = None
        self.image2 = None

        self.keypoint1 = None
        self.keypoint2 = None
        self.des1 = None
        self.des2 = None

        self.isCal = False

    def setPath(self, path):
        self.path = path

    def keypoints_calculate(self):
        self.image1 = cv2.imread(self.path + 'Shark1.jpg', 0)
        self.image2 = cv2.imread(self.path + 'Shark2.jpg', 0)

        orb = cv2.ORB_create()

        self.keypoint1, self.des1 = orb.detectAndCompute(self.image1, None)
        self.keypoint2, self.des2 = orb.detectAndCompute(self.image2, None)

        self.isCal = True


    def find_keypoints(self):
        if self.isCal == False:
            self.keypoints_calculate()

        image1 = cv2.drawKeypoints(self.image1, self.keypoint1, None)
        image2 = cv2.drawKeypoints(self.image2, self.keypoint2, None)

        cv2.imshow("find_keypoints (Shark1.jpg)", image1)
        cv2.imshow("find_keypoints (Shark2.jpg)", image2)

        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def matched_keypoints(self):
        if self.isCal == False:
            self.keypoints_calculate()

        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

        matches = bf.match(self.des1, self.des2)
        matches = sorted(matches, key=lambda x: x.distance)

        draw_params = dict(matchColor=(0, 255, 0), singlePointColor=(255, 0, 0), flags = 0)
        result = cv2.drawMatches(self.image2, self.keypoint2, self.image1, self.keypoint1, matches[:200], None, **draw_params)

        cv2.imshow("matched_keypoints", result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

