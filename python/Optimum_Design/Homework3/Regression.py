from GoldSearch import goldSearch
import matplotlib.pylab as plt
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

    def fletcherReevesMethod(self, start = [0, 0], iteration = 100):
        position = np.array(start, float)
        gradient = self.getGradient(position)
        s = -gradient

        for _ in range(iteration):
            _lambda, _, _ = goldSearch(lambda x: self.regressionFunction(position + x * s), 0, 50)
            newPosition = position + _lambda * s
            newGradient = self.getGradient(newPosition)
            beta = np.dot(newGradient, newGradient) / np.dot(gradient, gradient)
            newS = -newGradient + beta * s

            position = newPosition.copy()
            gradient = newGradient.copy()
            s = newS.copy()

        return position

    def newtonMethod(self, start = [0, 0], iteration = 100):
        position = np.array(start, float)

        for _ in range(iteration):
            position = position - np.dot(np.linalg.inv(self.getHessianMatrix(position)), self.getGradient(position).T).T

        return position


class quadraticRegression:

    def __init__(self, xData, yData):
        self.xData = xData
        self.yData = yData

    def regressionFunction(self, position):
        a0, a1, a2 = position
        return sum([(y - (a2 * x ** 2 + a1 * x + a0)) ** 2 for x, y in zip(self.xData, self.yData)])

    def getGradient(self, position):
        a0, a1, a2 = position
        d0 = sum([2 * (y - (a2 * x ** 2 + a1 * x + a0)) * (-1)      for x, y in zip(self.xData, self.yData)])
        d1 = sum([2 * (y - (a2 * x ** 2 + a1 * x + a0)) * (-x)      for x, y in zip(self.xData, self.yData)])
        d2 = sum([2 * (y - (a2 * x ** 2 + a1 * x + a0)) * (-x ** 2) for x, y in zip(self.xData, self.yData)])
        return np.array([d0, d1, d2], float)

    def getHessianMatrix(self, position):
        a0, a1, a2 = position
        d00 = sum([2 * (-1)      * (-1)      for x, y in zip(self.xData, self.yData)])
        d01 = sum([2 * (-x)      * (-1)      for x, y in zip(self.xData, self.yData)])
        d02 = sum([2 * (-x ** 2) * (-1)      for x, y in zip(self.xData, self.yData)])
        d10 = sum([2 * (-1)      * (-x)      for x, y in zip(self.xData, self.yData)])
        d11 = sum([2 * (-x)      * (-x)      for x, y in zip(self.xData, self.yData)])
        d12 = sum([2 * (-x ** 2) * (-x)      for x, y in zip(self.xData, self.yData)])
        d20 = sum([2 * (-1)      * (-x ** 2) for x, y in zip(self.xData, self.yData)])
        d21 = sum([2 * (-x)      * (-x ** 2) for x, y in zip(self.xData, self.yData)])
        d22 = sum([2 * (-x ** 2) * (-x ** 2) for x, y in zip(self.xData, self.yData)])
        return np.array([[d00, d01, d02], [d10, d11, d12], [d20, d21, d22]], float)

    def fletcherReevesMethod(self, start = [0, 0, 0], iteration = 100):
        position = np.array(start, float)
        gradient = self.getGradient(position)
        s = -gradient

        for _ in range(iteration):
            _lambda, _, _ = goldSearch(lambda x: self.regressionFunction(position + x * s), 0, 50)
            newPosition = position + _lambda * s
            newGradient = self.getGradient(newPosition)
            beta = np.dot(newGradient, newGradient) / np.dot(gradient, gradient)
            newS = -newGradient + beta * s

            position = newPosition.copy()
            gradient = newGradient.copy()
            s = newS.copy()

        return position

    def newtonMethod(self, start = [0, 0, 0], iteration = 100):
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


class constructRegression:

    def __init__(self, xData, yData):
        self.xData = xData
        self.yData = yData

    def regressionFunction(self, position):
        a0, a1, a2 = position
        return sum([(y - (a2 * np.sin(x) + a1 * x + a0)) ** 2 for x, y in zip(self.xData, self.yData)])

    def getGradient(self, position):
        a0, a1, a2 = position
        d0 = sum([2 * (y - (a2 * np.sin(10 * x) + a1 * x + a0)) * (-1)              for x, y in zip(self.xData, self.yData)])
        d1 = sum([2 * (y - (a2 * np.sin(10 * x) + a1 * x + a0)) * (-x)              for x, y in zip(self.xData, self.yData)])
        d2 = sum([2 * (y - (a2 * np.sin(10 * x) + a1 * x + a0)) * (-np.cos(10 * x)) for x, y in zip(self.xData, self.yData)])
        return np.array([d0, d1, d2], float)

    def fletcherReevesMethod(self, start = [0, 0, 0], iteration = 100):
        position = np.array(start, float)
        gradient = self.getGradient(position)
        s = -gradient

        for _ in range(iteration):
            _lambda, _, _ = goldSearch(lambda x: self.regressionFunction(position + x * s), 0, 50)
            newPosition = position + _lambda * s
            newGradient = self.getGradient(newPosition)
            beta = np.dot(newGradient, newGradient) / np.dot(gradient, gradient)
            newS = -newGradient + beta * s

            position = newPosition.copy()
            gradient = newGradient.copy()
            s = newS.copy()

        return position


def printFunction(coefficient, isPolynomial = True, d = 3):
    coefficient = [round(c, d) for c in coefficient]

    def printPolynomial(coefficient, d):
        printString = str(coefficient[0])
        for i in range(1, len(coefficient)):
            c = coefficient[i]
            symbol = "+" if c >= 0 else "-"
            printString += " {} {} x^{}".format(symbol, abs(c), i) if i != 1 else " {} {} x".format(symbol, abs(c))
        printString = "f(x) = " + printString
        return printString

    printString = printPolynomial(coefficient, d) if isPolynomial else "f(x) = {} sin(x) + {}x + {}".format(coefficient[2], coefficient[1], coefficient[0])
    print(printString)
    return printString


def plotData(xData, yData, title = "", function = None):

    def plotFunction():
        if not function:
            return
        X = np.linspace(0, 12, 100)
        Y = [function(x) for x in X]
        plt.plot(X, Y, label = "Regression Curve")

    data = np.array(sorted(zip(xData, yData)))
    plt.figure(figsize = (10, 6))
    plt.title(title)
    plt.plot(data[:, 0], data[:, 1], "-o", label = "Origin Data")
    plt.xlabel("x")
    plt.ylabel("y")
    plotFunction()
    plt.legend()
    plt.show()
