from turtle import position
from matplotlib.pyplot import vlines
import numpy as np

def dichotomousSearch(f, a, b, findMin = True, delta = 10 ** -7, tol = 10 ** -5):

    values = []

    while (b - a) > tol:

        lambda_ = a + (b - a) / 2
        mu = lambda_ + delta

        values.append(f(lambda_))
        if (values[-1] < f(mu)) == findMin:
            b = mu
        else:
            a = lambda_

    position = a + (b - a) / 2
    value = values[-1]

    return position, value, np.array(values)