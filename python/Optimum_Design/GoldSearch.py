import numpy as np

def goldSearch(f, a, b, findMin = True, tol = 10 ** -7):  

    R = (np.sqrt(5) - 1) / 2
    C = 1 - R
    x1 = R * a + C * b
    x2 = C * a + R * b
    f1 = f(x1)
    f2 = f(x2)

    values = []

    while (b - a) > tol:

        if findMin:
            values.append(min(f1, f2))
        else:
            values.append(max(f1, f2))

        if (f1 > f2) == findMin:
            a = x1
            x1 = x2
            f1 = f2
            x2 = C * a + R * b
            f2 = f(x2)
        else:
            b = x2
            x2 = x1
            f2 = f1
            x1 = R * a + C * b
            f1 = f(x1)
    
    if (f1 < f2) == findMin:
        fExtreme = f1
        xExtreme = x1
    else:
        fExtreme = f2
        xExtreme = x2
    values.append(fExtreme)

    return xExtreme, fExtreme, values