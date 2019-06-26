import numpy as np
import matplotlib.pylab as plt
from math import factorial

def Binomial(n,N,p):
    value = factorial(N)/((factorial(n))*(factorial(N-n)))
    value = value*(p**n)*((1-p)**(N-n))
    return value

def Gaussian(n,N,p):
    value = 1.0/(2*np.pi*p*(1-p)*N)**0.5
    value = value*np.e**(-((n-p*N)**2)/(2*p*(1-p)*N))
    return value

p=0.5
N=[10,100,1000]
color=["blue","green","red"]
for i in range(len(N)):
    B=[]
    G=[]
    n=np.linspace(0,1,N[i]+1)
    for j in range(N[i]+1):
        B.append(j*Binomial(j,N[i],p))
        G.append(j*Gaussian(j,N[i],p))
    plt.plot(n,B,"-o",color=color[i],label="Binomial N="+str(N[i]))
    plt.plot(n,G,"-o",color=color[i],label="Gaussian N="+str(N[i]))
plt.title("Binomial Distribution and Gaussian Distribution")
plt.xlabel("x")
plt.ylabel("nP(n|N)")
plt.legend()
plt.show()
    



