import numpy as np

def downhillSimplexSearch(f, start, rk = 0, iteration = 100, parameter = [1, 0.5, 2]):
    
    values = []
    alpha, beta, gamma = parameter
    positions = np.array(sorted(start, key = lambda position: f(position, rk)), float)
    minPositions = []

    while rk < 10 ** 10:

        for _ in range(iteration):           

            # Order
            positions = np.array(sorted(positions, key = lambda position: f(position, rk)), float)

            # Step 1
            xAvg = np.average(positions[:-1], axis = 0)
            xMin = positions[0]
            xMax = positions[-1]
            xSecondMax = positions[-2]
            minPositions.append(np.average(positions, axis = 0))
            values.append(f(xMin, rk))

            # Step 2
            xr = xAvg + alpha * (xAvg - xMax)
            if f(xMin, rk) > f(xr, rk):
                xe = xAvg + gamma * (xr - xAvg)

                # Step 3
                if f(xr, rk) > f(xe, rk):
                    positions[-1] = xe
                else:
                    positions[-1] = xr
                continue

            # Step 4
            if f(xSecondMax, rk) >= f(xr, rk):
                positions[-1] = xr
                continue
            
            # Step 5
            xp = min(xr, xMax, key = lambda x: f(x, rk))
            xc = xAvg + beta * (xp - xAvg)
            if f(xc, rk) > f(xp, rk):
                positions = [position + (xMin - position) / 2 for position in positions]
            else:
                positions[-1] = xc

        rk *= 10
        if rk == 0:
            break

    positions = np.array(sorted(positions, key = lambda position: f(position, rk)), float)
    xMin = positions[0]
    minPositions.append(np.average(positions, axis = 0))
    values.append(f(xMin, rk))

    return np.array(minPositions), np.array(values)