import numpy as np
from math import factorial
import matplotlib.pylab as plt

def Poisson_distribution(mu,N):
    def Poisson(mu,n):
        value = (mu**n)*(np.e**(-mu))/float(factorial(n))
        return value    
    probability=np.zeros(N+1,float)
    for i in range(N+1):
        probability[i] = Poisson(mu,i)
    return probability

def display(probability):
    plt.title("Poisson Distribution")
    plt.xlabel("number of n")
    plt.ylabel("probability")
    plt.xticks(range(len(probability)))
    plt.bar(range(len(probability)),probability,align='center',width=1,edgecolor="black")
    plt.show()

display(Poisson_distribution(10,20))
