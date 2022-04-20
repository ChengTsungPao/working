from GoldSearch import goldSearch
import numpy as np

class linearRegression:

    def __init__(self, xData, yData):
        self.xData = xData
        self.yData = yData

    def regressionFunction(self, position):
        a0, a1 = position
        return sum([(y - (a1 * x + a0)) ** 2 for x, y in zip(self.xData, self.yData)])

    def getGradient(self, position):
        a0, a1 = position
        d0 = sum([2 * (y - (a1 * x + a0)) * (-1) for x, y in zip(self.xData, self.yData)])
        d1 = sum([2 * (y - (a1 * x + a0)) * (-x) for x, y in zip(self.xData, self.yData)])
        return np.array([d0, d1], float)

    def getHessianMatrix(self, position):
        a0, a1 = position
        d00 = sum([2 * (-1) * (-1) for x, y in zip(self.xData, self.yData)])
        d01 = sum([2 * (-x) * (-1) for x, y in zip(self.xData, self.yData)])
        d10 = sum([2 * (-1) * (-x) for x, y in zip(self.xData, self.yData)])
        d11 = sum([2 * (-x) * (-x) for x, y in zip(self.xData, self.yData)])
        return np.array([[d00, d01], [d10, d11]], float)

    def fletcherReevesMethod(self, start = [0, 0], tol = 10 ** -5):
        position = np.array(start, float)
        gradient = self.getGradient(position)
        s = -gradient

        _lambda = float("inf")
        while _lambda > tol:
            _lambda, _, _ = goldSearch(lambda x: self.regressionFunction(position + x * s), 0, 50)
            newPosition = position + _lambda * s
            newGradient = self.getGradient(newPosition)
            beta = np.dot(newGradient, newGradient) / np.dot(gradient, gradient)
            newS = -newGradient + beta * s

            position = newPosition.copy()
            gradient = newGradient.copy()
            s = newS.copy()

        return position

    def newtonMethod(self, start = [0, 0], iteration = 10):
        position = np.array(start, float)

        for _ in range(iteration):
            position = position - np.dot(np.linalg.inv(self.getHessianMatrix(position)), self.getGradient(position).T).T

        return position


class polynomialRegression:

    def __init__(self, xData, yData):
        self.xData = xData
        self.yData = yData

    def getPolynomialMatrix(self, k):
        n = len(self.xData)
        matrix = np.zeros((n, k + 1), float)
        for i in range(n):
            x = 1
            for j in range(k + 1):
                matrix[i][j] = x
                x *= self.xData[i]
        return matrix

    def polynomialRegressionMethod(self, k):
        k = k if k >= 1 else 1
        x = self.getPolynomialMatrix(k)
        y = np.array(self.yData, float).T
        m = np.linalg.inv(np.dot(x.T, x))
        return (np.dot(np.dot(m, x.T), y)).T


def printPolynomial(constant, d = 5):
    ans = str(round(constant[0], d))
    for i in range(1, len(constant)):
        c = constant[i]
        symbol = "+" if c >= 0 else "-"
        ans += " {} {} x^{}".format(symbol, round(abs(c), d), i) if i != 1 else " {} {} x".format(symbol, round(abs(c), d))
    print("f(x) = {}".format(ans))