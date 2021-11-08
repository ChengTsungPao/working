import cv2


class image_smoothing():

    def __init__(self, path):
        self.setPath(path)


    def setPath(self, path):
        self.path = path
        self.lenna_pepperSalt_image = cv2.imread(self.path + "Lenna_pepperSalt.jpg")
        self.lenna_whiteNoise_image = cv2.imread(self.path + "Lenna_whiteNoise.jpg")


    def gaussian_blur(self):
        image_gaussian_five = cv2.GaussianBlur(self.lenna_whiteNoise_image, (5, 5), 0)

        cv2.imshow("5x5 Gaussian filter", image_gaussian_five)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def bilateral_filter(self):
        image_gaussian_nine = cv2.bilateralFilter(self.lenna_whiteNoise_image, 9, 90, 90)

        cv2.imshow("9x9 Bilateral filter", image_gaussian_nine)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def median_filter(self):
        image_median_three = cv2.medianBlur(self.lenna_pepperSalt_image, 3)
        image_median_five = cv2.medianBlur(self.lenna_pepperSalt_image, 5)

        cv2.imshow("3x3 median filter", image_median_three)
        cv2.imshow("5x5 median filter", image_median_five)
        cv2.waitKey(0)
        cv2.destroyAllWindows()