import numpy as np
import matplotlib.pylab as plt
from GoldSearch import goldSearch
from CyclicCoordinate import cyclicCoordinate

def f1(position):
    x = position
    return (x ** 3) * np.e ** (-x ** 2)

def f2(position):
    x1, x2 = position
    return (x1 ** 2 + x2 - 11) ** 2 + (x1 + x2 ** 2 - 7) ** 2

if __name__ == "__main__":

    # Problem 1 (goldSearch)
    print("Problem 1 (goldSearch)")
    xMin, fMin, valuesMin = goldSearch(f1, -2, 2, True)
    xMax, fMax, valuesMax = goldSearch(f1, -2, 2, False)
    print("  Local Min: position = {}, value = {}".format(xMin, fMin))
    print("  Local Max: position = {}, value = {}".format(xMax, fMax))
    print()

    plt.plot(list(range(1, len(valuesMin) + 1)), valuesMin, "-o")
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


    # Problem 3 (Powell’s conjugate direction method )
    print("Problem 3 (Powell’s conjugate direction method )")

    


