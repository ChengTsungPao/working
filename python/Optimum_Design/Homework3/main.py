from Regression import linearRegression, polynomialRegression, printPolynomial


if __name__ == "__main__":
    dataX = [0.1, 0.9, 1.9, 2.3, 3, 4.1, 5.2, 5.9, 6.8, 8.1, 8.7, 9.2, 10.1, 12]
    dataY = [20, 24, 27, 29, 32, 37.3, 36.4, 32.4, 28.5, 30, 38, 43, 40, 32]

    linearRegression_func = linearRegression(dataX, dataY)
    result = linearRegression_func.fletcherReevesMethod([0, 0])
    printPolynomial(result)
    result = linearRegression_func.newtonMethod([0, 0])
    printPolynomial(result)

    polynomialRegression_func = polynomialRegression(dataX, dataY)
    result = polynomialRegression_func.polynomialRegressionMethod(6)
    printPolynomial(result)
