import cv2
import numpy as np
import matplotlib.pylab as plt

class scale_invariant_feature_transform():

    def __init__(self, path):
        
        self.keypointsImage1 = None 
        self.keypointsImage2 = None
        self.matchResult = None
        self.combineImage = None
        self.path = path

        self.isCal = False


    def setPath(self, path):
        self.path = path


    def keypoints_calculate(self):
        image1 = cv2.imread(self.path + 'Shark2.jpg', 0)
        image2 = cv2.imread(self.path + 'Shark1.jpg', 0)

        ########################## find keypoint ##########################

        sift = cv2.xfeatures2d.SIFT_create()

        keypoint1, des1 = sift.detectAndCompute(image1, None)
        keypoint2, des2 = sift.detectAndCompute(image2, None)

        keypoint1, des1 = zip(*sorted(zip(keypoint1, des1), key = lambda x: x[0].size, reverse = True)[:200])
        keypoint2, des2 = zip(*sorted(zip(keypoint2, des2), key = lambda x: x[0].size, reverse = True)[:200])

        keypoint1, des1 = np.array(keypoint1), np.array(des1)
        keypoint2, des2 = np.array(keypoint2), np.array(des2)

        ########################## find keypoint ##########################

        flann = cv2.FlannBasedMatcher(dict(algorithm = 1, trees = 5), dict(checks = 50))

        matches = flann.knnMatch(des1, des2, k = 2)
        goodMatch = [m for m, n in matches if m.distance < 0.7 * n.distance]

        ########################## combine Image ##########################

        source_points = np.float32([keypoint1[m.queryIdx].pt for m in goodMatch]).reshape(-1, 1, 2)
        destination_points = np.float32([keypoint2[m.trainIdx].pt for m in goodMatch]).reshape(-1, 1, 2)
        M, mask = cv2.findHomography(source_points, destination_points, cv2.RANSAC, 5.0)
        combineImage = cv2.warpPerspective(image1, M, (image1.shape[1] + image2.shape[1], image1.shape[0]))
        combineImage[:image2.shape[0], :image2.shape[1]] = image2

        ########################### cache Image ###########################

        self.keypointsImage1 = cv2.drawKeypoints(image1, keypoint1, None)
        self.keypointsImage2 = cv2.drawKeypoints(image2, keypoint2, None)
        self.matchResult = cv2.drawMatchesKnn(self.keypointsImage1, keypoint1, self.keypointsImage2, keypoint2, np.expand_dims(goodMatch, 1), None)
        self.combineImage = combineImage

        self.isCal = True


    def find_keypoints(self):
        if self.isCal == False:
            self.keypoints_calculate()

        cv2.imshow("find_keypoints (Shark2.jpg)", self.keypointsImage1)
        cv2.imshow("find_keypoints (Shark1.jpg)", self.keypointsImage2)

        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def matched_keypoints(self):
        if self.isCal == False:
            self.keypoints_calculate()
        
        cv2.imshow("matched_keypoints", self.matchResult)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def matched_images(self):
        if self.isCal == False:
            self.keypoints_calculate()

        cv2.imshow("matched_images", self.combineImage)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
