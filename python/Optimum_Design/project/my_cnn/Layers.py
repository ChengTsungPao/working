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
        if self.input == []:
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


class MaxPool2D:
    def __init__(self, size = 2):
        self.size = size
        self.input = []

    def __call__(self, input):
        return self.forward(input)

    def getImageRegions(self, image):
        h, w, _ = image.shape
        for i in range(h // self.size):
            for j in range(w // self.size):
                region = image[self.size * i: self.size * (i + 1), self.size * j: self.size * (j + 1)]
                yield region, i, j

    def forward(self, input):
        self.input = input

        h, w, filter = input.shape
        output = np.zeros((h // self.size, w // self.size, filter))

        for region, i, j in self.getImageRegions(input):
            output[i, j] = np.amax(region, axis=(0, 1))

        return output

    def backprop(self, gradient):
        if self.input == []:
            print("Require run forward first !!!")
            return

        newGradient = np.zeros(self.input.shape)

        # fill gradient in origin max value position
        for region, i, j in self.getImageRegions(self.input):
            h, w, f = region.shape
            max_ = np.amax(region, axis=(0, 1))

            for di in range(h):
                for dj in range(w):
                    for df in range(f):
                        if region[di, dj, df] == max_[df]:
                            newGradient[i * 2 + di, j * 2 + dj, df] = gradient[i, j, df]

        return newGradient


class Conv2D:
    def __init__(self, in_channel, filter, size, padding) -> None:
        self.size = size
        self.filter = filter
        self.padding = padding
        self.kernel = np.random.randn(self.size, self.size, filter) / (self.size * self.size)
        self.input = []

    def __call__(self, input):
        return self.forward(input)

    def getImageRegions(self, image):
        h, w, _ = image.shape
        for i in range(h - self.size + 1):
            for j in range(w - self.size + 1):
                region = image[i: i + self.size, j: j + self.size]
                yield region, i, j

    def forward(self, input):
        self.input = input
        input = np.pad(input, ((self.padding, self.padding), (self.padding, self.padding), (0, 0)))

        h, w, _ = input.shape
        output = np.zeros((h - self.size + 1, w - self.size + 1, self.filter))

        for region, i, j in self.getImageRegions(input):
            output[i, j] = np.sum(self.kernel * region, axis=(0, 1))

        return output

    def backprop(self, gradient, learning_rate):
        if self.input == []:
            print("Require run forward first !!!")
            return

        newGradient = np.zeros(self.kernel.shape)

        for region, i, j in self.getImageRegions(self.input):
            for f in range(self.filter):
                newGradient[:, :, f:f+1] += gradient[i, j, f] * region

        self.kernel -= learning_rate * newGradient
        return newGradient


class Linear:
    def __init__(self, in_dim, out_dim):
        self.weight = np.random.rand(out_dim, in_dim)
        self.basis = np.random.rand(out_dim, 1)

    def __call__(self, input):
        return self.forward(input)

    def forward(self, input):
        self.input = input
        input = input.reshape(-1, 1)
        output = np.dot(self.weight, input) + self.basis
        return output.T[0]

    def backprop(self, gradient, learning_rate):

        dw = np.dot(gradient.reshape(self.basis.shape), self.input.reshape(-1, 1).T)
        db = gradient.reshape(self.basis.shape)

        self.weight -= learning_rate * dw
        self.basis -= learning_rate * db

        dout = np.dot(self.weight.T, gradient.reshape(self.basis.shape))
        return dout.reshape(self.input.shape)


