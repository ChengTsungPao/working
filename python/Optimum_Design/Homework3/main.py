from Regression import linearRegression, quadraticRegression, polynomialRegression, constructRegression, printFunction, plotData
import numpy as np

if __name__ == "__main__":
    dataX = [0.1, 0.9, 1.9, 2.3, 3, 4.1, 5.2, 5.9, 6.8, 8.1, 8.7, 9.2, 10.1, 12]
    dataY = [20, 24, 27, 29, 32, 37.3, 36.4, 32.4, 28.5, 30, 38, 43, 40, 32]

    ############################################ Problem 2 #############################################
    print("\nProblem 2")
    linearRegression_func = linearRegression(dataX, dataY)
    coefficient = linearRegression_func.fletcherReevesMethod([0, 0])
    printString = printFunction(coefficient)
    plotData(dataX, dataY, printString, lambda x: sum([a * x ** k for k, a in enumerate(coefficient)]))
    coefficient = linearRegression_func.newtonMethod([0, 0])
    printString = printFunction(coefficient)
    plotData(dataX, dataY, printString, lambda x: sum([a * x ** k for k, a in enumerate(coefficient)]))

    ############################################ Problem 3 #############################################
    print("\nProblem 3")
    quadraticRegression_func = quadraticRegression(dataX, dataY)
    coefficient = quadraticRegression_func.fletcherReevesMethod([0, 0, 0])
    printString = printFunction(coefficient)
    plotData(dataX, dataY, printString, lambda x: sum([a * x ** k for k, a in enumerate(coefficient)]))
    coefficient = quadraticRegression_func.newtonMethod([0, 0, 0])
    printString = printFunction(coefficient)
    plotData(dataX, dataY, printString, lambda x: sum([a * x ** k for k, a in enumerate(coefficient)]))
    
    polynomialRegression_func = polynomialRegression(dataX, dataY)
    coefficient = polynomialRegression_func.polynomialRegressionMethod(5)
    printString = printFunction(coefficient)
    plotData(dataX, dataY, printString, lambda x: sum([a * x ** k for k, a in enumerate(coefficient)]))

    ############################################ Problem 4 #############################################
    print("\nProblem 4")
    constructRegression_func = constructRegression(dataX, dataY)
    coefficient = constructRegression_func.fletcherReevesMethod()
    printString = printFunction(coefficient, False)
    plotData(dataX, dataY, printString, lambda x: coefficient[2] * np.sin(x) + coefficient[1] * x + coefficient[0])