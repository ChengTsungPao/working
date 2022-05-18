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

    for iter in range(iteration):

        # Order
        positions = np.array(sorted(positions, key = lambda position: f(position)), float)

        # Step 1
        xAvg = np.average(positions[:-1], axis = 0)
        xMin = positions[0]
        xMax = positions[-1]
        xSecondMax = positions[-2]
        minPositions.append(np.average(positions, axis = 0))
        values.append(f(xMin))

        # Step 2
        xr = xAvg + alpha * (xAvg - xMax)
        if f(xMin) > f(xr):
            xe = xAvg + gamma * (xr - xAvg)

            # Step 3
            if f(xr) > f(xe):
                positions[-1] = xe
            else:
                positions[-1] = xr
            continue

        # Step 4
        if f(xSecondMax) >= f(xr):
            positions[-1] = xr
            continue
        
        # Step 5
        xp = min(xr, xMax, key = lambda x: f(x))
        xc = xAvg + beta * (xp - xAvg)
        if f(xc) > f(xp):
            positions = [position + (xMin - position) / 2 for position in positions]
        else:
            positions[-1] = xc

    positions = np.array(sorted(positions, key = lambda position: f(position)), float)
    xMin = positions[0]
    minPositions.append(np.average(positions, axis = 0))
    values.append(f(xMin))

    return np.array(minPositions), np.array(values)