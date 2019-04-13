import numpy as np
import random
import matplotlib.pylab as plt

def dise(sides,trials,N):
    histogram = np.zeros(sides*N-N+1 , int)
    sum = 0.0
    j=0
    r=0
    while j < trials :
        sum = 0
        for i in range(N):
            r=int(random.random()*sides)+1
            sum+=r  
        histogram[sum-N] = histogram[sum-N] + 1
        j=j+1
    return histogram

plt.subplot(121)
N=2
sides=6
trials=100000
dise_sum=range(1*N,sides*N+1)
probability=dise(sides,trials,N)/float(trials)
plt.title("Probability Distribution of dises")
plt.xlabel("sum of the dises")
plt.ylabel("probability")
plt.xticks(dise_sum)
plt.plot(dise_sum,probability,"-o",label="N="+str(N)+" sides="+str(sides))
plt.legend()

plt.subplot(122)
N=3
sides=6
trials=100000
dise_sum=range(1*N,sides*N+1)
probability=dise(sides,trials,N)/float(trials)
plt.title("Probability Distribution of dises")
plt.xlabel("sum of the dises")
plt.ylabel("probability")
plt.xticks(dise_sum)
plt.plot(dise_sum,probability,"-o",label="N="+str(N)+" sides="+str(sides))
plt.legend()

plt.tight_layout()
plt.show()