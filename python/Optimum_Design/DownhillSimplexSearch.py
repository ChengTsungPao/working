from turtle import pos
import numpy as np

def downhillSimplexSearch(f, start, iteration = 100, parameter = [1, 0.5, 2]):

    values = []
    alpha, beta, gamma = parameter
    positions = np.array(sorted(start, key = lambda position: f(position)), float)
    minPositions = []

    for _ in range(iteration):

        # Order
        positions = np.array(sorted(positions, key = lambda position: f(position)), float)

        # Calculate x0
        x0 = np.average(positions[:-1], axis = 0)
        x1 = positions[0]
        xn = positions[-2]
        xn_1 = positions[-1]
        minPositions.append(x0)
        values.append(f(x1))

        # Reflection
        xr = x0 + alpha * (x0 - xn_1)
        if f(x0) <= f(xr) < f(xn):
            positions[-1] = xr
            continue

        # Expansion
        if f(xr) < f(x1):
            xe = x0 + gamma * (xr - x0)
            if f(xe) < f(xr):
                positions[-1] = xe
            else:
                positions[-1] = xr
            continue

        # Contraction
        if f(xr) >= f(xn):
            if f(xr) < f(xn_1):
                xc = x0 + beta * (xr - x0)
                if f(xc) < f(xr):
                    positions[-1] = xc
                    continue
            else:
                xc = x0 + beta * (xn_1 - x0)                
                if f(xc) < f(xn_1):
                    positions[-1] = xc
                    continue    

        # Shrink
        for i in range(1, len(positions)):
            xi = positions[i]
            positions[i] = x1 + beta * (xi - x1)    

    return np.array(minPositions), np.array(values)



