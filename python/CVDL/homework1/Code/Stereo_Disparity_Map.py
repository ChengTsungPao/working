import cv2

class stereo_disparity_map():

    def stereo_disparity_map(self, path):
        # Load the left and right images in gray scale
        imgLeft = cv2.imread(path + 'imL.png', 0)
        imgRight = cv2.imread(path + 'imR.png', 0)

        # Initialize the stereo block matching object 
        # stereo = cv2.StereoBM_create(numDisparities=16, blockSize=5)
        stereo = cv2.StereoBM(1, 16, 15)
        # stereo = cv2.createStereoBM(numDisparities=16, blockSize=15)

        # Compute the disparity image
        disparity = stereo.compute(imgLeft, imgRight)

        # Normalize the image for representation
        min = disparity.min()
        max = disparity.max()
        disparity = np.uint8(6400 * (disparity - min) / (max - min))

        # Display the result
        cv2.imshow('disparittet', np.hstack((imgLeft, imgRight, disparity)))
        cv2.waitKey(0)
        cv2.destroyAllWindows()