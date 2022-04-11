import numpy as np
import matplotlib.pylab as plt
from GoldSearch import goldSearch
from DichotomousSearch import dichotomousSearch
from CyclicCoordinate import cyclicCoordinate
from DownhillSimplexSearch import downhillSimplexSearch

def f1(position):
    x = position
    return (x ** 3) * np.e ** (-x ** 2)

def f2(position):
    x1, x2 = position
    return (x1 ** 2 + x2 - 11) ** 2 + (x1 + x2 ** 2 - 7) ** 2

if __name__ == "__main__":

    # Problem 1 (dichotomousSearch)
    print("Problem 1 (dichotomousSearch)")
    xMinG, fMinG = goldSearch(f1, -2, 2, True)
    xMaxG, fMaxG = goldSearch(f1, -2, 2, False)
    xMinD, fMinD, valuesMin = dichotomousSearch(f1, -2, 2, True)
    xMaxD, fMaxD, valuesMax = dichotomousSearch(f1, -2, 2, False)
    print("  Local Min: position = {}, value = {} (goldSearch)".format(xMinG, fMinG))
    print("  Local Max: position = {}, value = {} (goldSearch)".format(xMaxG, fMaxG))
    print("  Local Min: position = {}, value = {} (dichotomousSearch)".format(xMinD, fMinD))
    print("  Local Max: position = {}, value = {} (dichotomousSearch)".format(xMaxD, fMaxD))
    print()

    plt.plot(list(range(1, len(valuesMin) + 1)), valuesMin, "-o")
    plt.xticks(list(range(1, len(valuesMin) + 1, 1)))
    plt.show()


    # Problem 2 (cyclic coordinate method)
    print("Problem 2 (cyclic coordinate method)")
    positions1, values1 = cyclicCoordinate(f2, [3, 4])
    positions2, values2 = cyclicCoordinate(f2, [-3, -4])
    print("  Local Min: position = {}, value = {}".format(tuple(positions1[-1]), values1[-1]))
    print("  Local Min: position = {}, value = {}".format(tuple(positions2[-1]), values2[-1]))
    print()

    plt.plot(positions1[:, 0], positions1[:, 1], "-o")
    plt.show()


    # Problem 3 (Nelder-Mead downhill simplex method)
    print("Problem 3 (Nelder-Mead downhill simplex method)")
    positions1, values1 = downhillSimplexSearch(f2, [[3, 4], [4, 4], [3, 3]])
    positions2, values2 = downhillSimplexSearch(f2, [[-3, -4], [-4, -4], [-3, -3]])
    print("  Local Min: position = {}, value = {}".format(tuple(positions1[-1]), values1[-1]))
    print("  Local Min: position = {}, value = {}".format(tuple(positions2[-1]), values2[-1]))

    plt.plot(positions1[:, 0], positions1[:, 1], "-o")
    plt.show()

    


