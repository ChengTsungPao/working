import numpy as np


def x(a):
    sum = 0
    for i in range(len(a)):
        sum+=a[i]
    mu = sum/len(a)
    sum = 0
    for i in range(len(a)):
        sum += (a[i]-mu)**2
    v= (sum/len(a))**0.5
    return mu**(v+mu+1)



print(x([2,2,2,3,3]))       

    