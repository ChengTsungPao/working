import numpy as np
import cv2


class image_processing():

    def __init__(self, path):
        self.setPath(path)


    def setPath(self, path):
        self.path = path
        self.sun_image = cv2.imread(self.path + "Sun.jpg")
        self.dog_strong_image = cv2.imread(self.path + "Dog_Strong.jpg")
        self.dog_weak_image = cv2.imread(self.path + "Dog_Weak.jpg")


    def load_image(self):
        cv2.imshow("Sun.jpg", self.sun_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def color_separation(self):
        B_channel, G_channel, R_channel = cv2.split(self.sun_image)
        zeros = np.zeros(np.shape(B_channel), dtype = "uint8")

        cv2.imshow("B_channel", cv2.merge([B_channel, zeros, zeros]))
        cv2.imshow("G_channel", cv2.merge([zeros, G_channel, zeros]))
        cv2.imshow("R_channel", cv2.merge([zeros, zeros, R_channel]))
        
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def color_transformation(self):
        gray_weight = cv2.cvtColor(self.sun_image, cv2.COLOR_BGR2GRAY)
        gray_average = np.array((self.sun_image[:, :, 0] * (1 / 3)  + self.sun_image[:, :, 1] * (1 / 3) + self.sun_image[:, :, 2] * (1 / 3)), dtype = "uint8")

        cv2.imshow("OpenCV function", gray_weight)
        cv2.imshow("Average weighted", gray_average)

        cv2.waitKey(0)
        cv2.destroyAllWindows()   


    def combine_image(self, blend):
        dog_strong_weight = (255 - blend) / 255
        dog_weak_weight= blend / 255

        image = cv2.addWeighted(self.dog_strong_image, dog_strong_weight, self.dog_weak_image, dog_weak_weight, 0)
        cv2.imshow("color transformation", image)


    def blending(self):
        cv2.imshow("color transformation", self.dog_strong_image)
        cv2.createTrackbar("blend", "color transformation", 0, 255, self.combine_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()   

