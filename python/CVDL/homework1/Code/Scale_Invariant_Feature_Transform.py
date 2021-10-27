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

        self.goodMatch = None
        self.matchResult = None

        self.isCal = False


    def setPath(self, path):
        self.path = path


    def keypoints_calculate(self):
        self.image1 = cv2.imread(self.path + 'Shark2.jpg', 0)
        self.image2 = cv2.imread(self.path + 'Shark1.jpg', 0)

        ########################## find keypoint ##########################

        sift = cv2.xfeatures2d.SIFT_create()

        self.keypoint1, self.des1 = sift.detectAndCompute(self.image1, None)
        self.keypoint2, self.des2 = sift.detectAndCompute(self.image2, None)

        self.keypoint1, self.des1 = zip(*sorted(zip(self.keypoint1, self.des1), key = lambda x: x[0].size, reverse = True)[:200])
        self.keypoint2, self.des2 = zip(*sorted(zip(self.keypoint2, self.des2), key = lambda x: x[0].size, reverse = True)[:200])

        self.keypoint1, self.des1 = np.array(self.keypoint1), np.array(self.des1)
        self.keypoint2, self.des2 = np.array(self.keypoint2), np.array(self.des2)

        ########################## find keypoint ##########################

        flann = cv2.FlannBasedMatcher(dict(algorithm = 1, trees = 5), dict(checks = 50))

        self.matches = flann.knnMatch(self.des1, self.des2, k = 2)
        self.goodMatch = [m for m, n in self.matches if m.distance < 0.7 * n.distance]
        self.goodMatch = np.expand_dims(self.goodMatch, 1)

        self.image1 = cv2.drawKeypoints(self.image1, self.keypoint1, None)
        self.image2 = cv2.drawKeypoints(self.image2, self.keypoint2, None)
        self.matchResult = cv2.drawMatchesKnn(self.image1, self.keypoint1, self.image2, self.keypoint2, self.goodMatch, None)

        self.isCal = True


    def find_keypoints(self):
        if self.isCal == False:
            self.keypoints_calculate()

        cv2.imshow("find_keypoints (Shark2.jpg)", self.image1)
        cv2.imshow("find_keypoints (Shark1.jpg)", self.image2)

        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def matched_keypoints(self):
        if self.isCal == False:
            self.keypoints_calculate()
        
        cv2.imshow("matched_keypoints", self.matchResult)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

