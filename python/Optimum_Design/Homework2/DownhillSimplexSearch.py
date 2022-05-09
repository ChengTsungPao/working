from turtle import pos, position
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
        minPositions.append(np.average(positions, axis = 0))
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


def downhillSimplexSearchTeacher(f, start, iteration = 100, parameter = [1, 0.5, 2]):
    
    values = []
    alpha, beta, gamma = parameter
    positions = np.array(sorted(start, key = lambda position: f(position)), float)
    minPositions = []

    for _ in range(iteration):

        print("============================= iteration = {} =============================".format(iteration))

        # Order
        positions = np.array(sorted(positions, key = lambda position: f(position)), float)

        # Step 1
        xAvg = np.average(positions[:-1], axis = 0)
        xMin = positions[0]
        xMax = positions[-1]
        xSecondMax = positions[-2]
        minPositions.append(np.average(positions, axis = 0))
        values.append(f(xMin))
        print("Step 1 => xMin = {}, xMax = {}, xSecondMax = {}, xAvg = {} (No xMax)".format(xMin, xMax, xSecondMax, xAvg))

        # Step 2
        xr = xAvg + alpha * (xAvg - xMax)
        if f(xMin) <= f(xr): 
            print("\nBecause: f(xMin) = {} <= f(xr) = {}".format(f(xMin), f(xr)))
            print("Step 2 => xr = {}".format(xr))

        if f(xMin) > f(xr):
            xe = xAvg + gamma * (xr - xAvg)
            print("\nBecause: f(xMin) = {} > f(xr) = {}".format(f(xMin), f(xr)))
            print("Step 2 => xr = {}, xe = {}".format(xr, xe))

            # Step 3
            if f(xr) > f(xe):
                print("\nBecause: f(xr) = {} > f(xe) = {}".format(f(xr), f(xe)))
                print("Step 3 => xMax = xe = {}".format(xe))
                positions[-1] = xe
            else:
                print("\nBecause: f(xr) = {} <= f(xe) = {}".format(f(xr), f(xe)))
                print("Step 3 => xMax = xr = {}".format(xr))
                positions[-1] = xr
            continue

        # Step 4
        if f(xSecondMax) >= f(xr):
            print("\nBecause: f(xSecondMax) = {} >= f(xr) = {}".format(f(xSecondMax), f(xr)))
            print("Step 4 => xMax = xr = {}".format(xr))
            positions[-1] = xr
            continue
        
        # Step 5
        xp = min(xr, xMax, key = lambda x: f(x))
        xc = xAvg + beta * (xp - xAvg)
        if f(xc) > f(xp):
            positions = [position + (xMin - position) / 2 for position in positions]
            print("\nBecause: f(xc) = {} > f(xp) = {}".format(f(xc), f(xp)))
            print("Step 5 => position = position + (xMin - position) / 2 = {}".format(positions))
        else:
            print("\nBecause: f(xc) = {} > f(xr) = {}".format(f(xc), f(xp)))
            print("Step 5 => xMax = xc = {}".format(xc))
            positions[-1] = xc

    return np.array(minPositions), np.array(values)


def f(position):
    x = position
    return x / (1 + x ** 2)

if __name__ == "__main__":
    positions1, values1 = downhillSimplexSearchTeacher(f, [-2, 0, -2], 2)
    print("\nlocal min value = {}".format(values1[-1]))
