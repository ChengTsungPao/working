from turtle import pos
from GoldSearch import goldSearch
import numpy as np

def cyclicCoordinate(f, start):
    
    def function_1D(lambda_):
        return f(position + lambda_ * vector)

    def distance(a, b):
        return sum((a - b) ** 2) ** 0.5

    dim = len(start)
    prePosition = np.array([float("inf"), float("inf")])
    position = np.array(start)

    positions = [position]
    values = [f(position)]

    while distance(prePosition, position) > 10 ** -5:
        # print(distance(prePosition, position))
        
        for d in range(dim):
            # search direction
            vector = np.zeros(dim)
            vector[d] = 1

            # find 1D function Min
            lambda_, value = goldSearch(function_1D, -20, 20)

            # get next position
            prePosition = position
            position = position + lambda_ * vector
            
            # save position and value
            positions.append(position)
            values.append(value)

    return np.array(positions), np.array(values)

    

    

    