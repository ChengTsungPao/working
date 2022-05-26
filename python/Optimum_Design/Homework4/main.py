from tracemalloc import start
from DownhillSimplexSearch import downhillSimplexSearch

import numpy as np
import warnings
warnings.filterwarnings("ignore")

########################################## Function1 ##########################################

def getFunction1Pos(position):
    r = position
    h = 20 / (np.pi * r * r)
    return [r, h]

def f1(position, rk):
    r, h = getFunction1Pos(position)
    return 2 * np.pi * r * r + 2 * np.pi * r * h

########################################## Function2 ##########################################

def getFunction2Pos(position):
    d = [None, 0.0298, 0.044, {"a": 0.044, "k": 0.0138}, 0.0329, {"k": 0.0329, "h": 0.0279}, 0.025, {"k": 0.025, "h": 0.0619}, 0.0317, 0.0368]
    M = [None, 4, 33, 31]

    F2, F3, F4, F5, F7, F8 = position
    F1 = (d[2] * F2 + d[3]["a"] * F3 + M[1]) / d[1]
    F6 = (-d[3]["k"] * F3 + d[4] * F4 + d[5]["k"] * F5 - d[7]["k"] * F7 - M[2]) / d[6]
    F9 = (d[5]["h"] * F5 - d[7]["h"] * F7 + d[8] * F8 - M[3]) / d[9]
    return [F1, F2, F3, F4, F5, F6, F7, F8, F9]

def getFunction2Val(position):
    A = [None, 11.5, 92.5, 44.3, 98.1, 20.1, 6.1, 45.5, 31.0, 44.3]
    F = [None] + getFunction2Pos(position)
    return sum([(F[i] / A[i]) ** 2 for i in range(1, 9 + 1)])

def f2(position, rk):
    A = [None, 11.5, 92.5, 44.3, 98.1, 20.1, 6.1, 45.5, 31.0, 44.3]
    F = [None] + getFunction2Pos(position)
    return sum([(F[i] / A[i]) ** 2 + rk * max(-F[i], 0) ** 2 for i in range(1, 9 + 1)])

if __name__ == "__main__":

    ########################################## Problem1 ##########################################

    print("\nProblem1")
    positions1, values1 = downhillSimplexSearch(f1, [1, 3, 2])
    print("  [r, h] = {}".format(getFunction1Pos(positions1[-1])))
    print("  A = {}".format(values1[-1]))

    ########################################## Problem2 ##########################################

    startF = [[13, 19,  2,  1, 10, 13],
              [ 8, 15, 10, 15, 13, 13],
              [18,  8,  1,  8, 19,  7],
              [16, 15, 19, 16,  4, 17],
              [10, 20, 13,  9, 15, 20],
              [17, 11,  1,  9, 12, 20]]

    print("\nProblem2")
    startF = list(startF) + [np.average(startF, axis = 0)]
    positions2, values2 = downhillSimplexSearch(f2, startF, 1)
    print("  F = {}".format(getFunction2Pos(positions2[-1])))
    print("  Z = {}".format(getFunction2Val(positions2[-1])))

    ########################################## Problem2 (Best Answer) ##########################################

    print("\nProblem2 (Best Answer)")
    value = float("inf")
    positions = None
    for _ in range(10):
        startF = np.random.randint(1, 100, size=(6, 6))
        startF = list(startF) + [np.average(startF, axis = 0)]
        positions2, values2 = downhillSimplexSearch(f2, startF, 1)
        if value > getFunction2Val(positions2[-1]) and all([pos >= 0 for pos in positions2[-1]]):
            value = getFunction2Val(positions2[-1])
            positions = positions2[-1]

    print("  F = {}".format(getFunction2Pos(positions)))
    print("  Z = {}".format(getFunction2Val(positions)))