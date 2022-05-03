import numpy as np

class Softmax:
    def __init__(self):
        self.input = []
    
    def __call__(self, input):
        return self.forward(input)

    def forward(self, input):
        self.input = input
        exp = np.exp(input)
        return exp / np.sum(exp, axis=0)

    def backprop(self, gradient):
        if not self.input:
            print("Require run forward first !!!")
            return

        for i in range(len(gradient)):
            if gradient[i] == 0:
                continue

            exp = np.exp(self.input)
            S = np.sum(exp)

            newGradient = -exp[i] * exp / (S ** 2)
            newGradient[i] = exp[i] * (S - exp[i]) / (S ** 2)

            newGradient = gradient * newGradient

            return newGradient.reshape(self.input.shape)


class MaxPool:
    def __init__(self, size = 2):
        self.size = size
        self.input = []

    def __call__(self, input):
        return self.forward(input)

    def getImageRegions(self, image):
        h, w, _ = image.shape
        for i in range(h // 2):
            for j in range(w // 2):
                region = image[self.size * i: self.size * (i + 1), self.size * j: self.size * (j + 1)]
                yield region, i, j

    def forward(self, input):
        self.input = input

        h, w, filter = input.shape
        output = np.zeros((h - self.size, w - self.size, filter))

        for region, i, j in self.getImageRegions(input):
            output[i, j] = np.amax(region, axis=(0, 1))

        return output

    def backprop(self, gradient):
        if not self.input:
            print("Require run forward first !!!")
            return

        for region, i, j in self.getImageRegions(input):
            h, w, f = region.shape
            # output[i, j] = np.amax(region, axis=(0, 1))


