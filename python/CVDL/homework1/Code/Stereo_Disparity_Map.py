import cv2
import numpy as np

class stereo_disparity_map():

    def stereo_disparity_map(self, path):
        # for i in np.arange(5, 12, 2):
        # Load the left and right images in gray scale
        imgLeft = cv2.imread(path + 'imL.png', 0)
        imgRight = cv2.imread(path + 'imR.png', 0)

        # Initialize the stereo block matching object 
        stereo = cv2.StereoBM_create(numDisparities=256, blockSize=25)
        # stereo = cv2.StereoBM(1, 16, 15)
        # stereo = cv2.createStereoBM(numDisparities=16, blockSize=15)

        # Compute the disparity image
        disparity = stereo.compute(imgLeft, imgRight)

        # # Normalize the image for representation
        min = disparity.min()
        max = disparity.max()
        # print(min, max)
        # disparity = 255 * (disparity - min) / (max - min)
        disparity = cv2.normalize(disparity, disparity, 255, 0, cv2.NORM_MINMAX)

        # focal = 4019.284
        # baseline = 342.789
        # depth = (baseline * focal) / (disparity)

        # Display the result
        showImage = np.hstack((imgLeft, imgRight, disparity))
        showImage = disparity
        shape = np.shape(showImage)
        showImage = cv2.resize(showImage, (shape[1] // 3, shape[0] // 3), interpolation=cv2.INTER_AREA)


        cv2.imshow('disparittet', showImage)
        cv2.waitKey(0)
        cv2.destroyAllWindows()