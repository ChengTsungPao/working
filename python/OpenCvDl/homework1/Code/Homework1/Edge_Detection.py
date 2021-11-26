import numpy as np
import cv2, copy


class edge_detection():

    def __init__(self, path):
        self.setPath(path)


    def setPath(self, path):
        self.path = path
        self.house_image = cv2.imread(self.path + "House.jpg", 0)
        self.sobelX_image = []
        self.sobelY_image = []
        self.gaussian_image = []


    def restrict_value(self, val):
        return min(abs(val), 255)


    def get_gaussian_kernel(self, kernel_size = 3):

        def G(x, y):
            sigma = 2 ** (-0.5)
            times = - (x ** 2 + y ** 2) / (2 * sigma ** 2)
            return (np.e ** times) / (2 * np.pi * sigma ** 2)

        kernel_filter = np.zeros((3, 3))
        kernel_size = 3

        for i in range(kernel_size):
            for j in range(kernel_size):
                x, y = i - kernel_size // 2, j - kernel_size // 2
                kernel_filter[i][j] = G(x, y)

        return kernel_filter / np.sum(kernel_filter)


    def gaussian_blur(self, kernel_size = 3, visible = True):
        padding = (kernel_size - 1) // 2
        kernel_filter = self.get_gaussian_kernel(kernel_size)
        padding_house_image = np.pad(self.house_image, padding)
        self.gaussian_image = copy.deepcopy(self.house_image) 

        for i in range(len(padding_house_image) - 2 * padding):
            for j in range(len(padding_house_image[0]) - 2 * padding):
                self.gaussian_image[i][j] = self.restrict_value(np.sum(padding_house_image[i : i + 3, j : j + 3] * kernel_filter))

        if visible:
            self.showImage("gaussian blur", self.gaussian_image)


    def sobelX(self, visible = True):
        if self.gaussian_image == []:
            self.gaussian_blur(visible = False)

        horizontal = [
            [ -1,  0,  1  ],
	        [ -2,  0,  2  ],
	        [ -1,  0,  1  ]
        ] 

        padding = (len(horizontal) - 1) // 2
        padding_gaussian_image = np.pad(self.gaussian_image, padding)
        self.sobelX_image = copy.deepcopy(self.gaussian_image) 

        for i in range(len(padding_gaussian_image) - 2 * padding):
            for j in range(len(padding_gaussian_image[0]) - 2 * padding):
                self.sobelX_image[i][j] = self.restrict_value(np.sum(padding_gaussian_image[i : i + 3, j : j + 3] * horizontal))

        if visible:
            self.showImage("sobelX", self.sobelX_image)


    def sobelY(self, visible = True):
        if self.gaussian_image == []:
            self.gaussian_blur(visible = False)

        vertical = [
            [  1,  2,  1  ],
	        [  0,  0,  0  ],
	        [ -1, -2, -1  ]
        ] 

        padding = (len(vertical) - 1) // 2
        padding_gaussian_image = np.pad(self.gaussian_image, padding)
        self.sobelY_image = copy.deepcopy(self.gaussian_image) 

        for i in range(len(padding_gaussian_image) - 2 * padding):
            for j in range(len(padding_gaussian_image[0]) - 2 * padding):
                self.sobelY_image[i][j] = self.restrict_value(np.sum(padding_gaussian_image[i : i + 3, j : j + 3] * vertical))

        if visible:
            self.showImage("sobelY", self.sobelY_image)


    def magnitude(self, visible = True):
        if self.sobelX_image == []:
            self.sobelX(False)

        if self.sobelY_image == []:
            self.sobelY(False)

        magnitude = copy.deepcopy(self.house_image) 

        for i in range(len(magnitude)):
            for j in range(len(magnitude[0])):
                magnitude[i][j] = self.restrict_value((self.sobelX_image[i][j] ** 2 + self.sobelY_image[i][j] ** 2) ** 0.5)

        if visible:
            self.showImage("magnitude", magnitude)


    def showImage(self, title, image):
        cv2.imshow(title, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()