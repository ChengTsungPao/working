import numpy as np
from math import factorial
import matplotlib.pylab as plt

def N_order(N):
    try:
        value = factorial(N)
    except:
        value = (np.e**(-N))*(N**N)*((2*np.pi*N+np.pi/3)**0.5)
    return value
    
def Binomial_distribution(p,N):
    def Binomial(n,N,p):
        value = N_order(N)/((N_order(n))*(N_order(N-n)))
        value = value*(p**n)*((1-p)**(N-n))
        return value   
    probability=np.zeros(N+1,float)
    for i in range(N+1):
        probability[i] = Binomial(i,N,p)
    return probability

def Poisson_distribution(mu,N):
    def Poisson(mu,n):
        value = (mu**n)*(np.e**(-mu))/float(N_order(n))
        return value    
    probability=np.zeros(N+1,float)
    for i in range(N+1):
        probability[i] = Poisson(mu,i)
    return probability

def display(probability1,probability2,data):
    plt.title("Poisson Distribution vs Binomial Distribution (N="+str(data[1])+" \u03BC=pN)")
    plt.xlabel("number of \u03BC and n")
    plt.ylabel("probability")
    plt.plot(range(len(probability1)),probability1,color="blue",label="Poisson   p="+str(data[2]))
    plt.plot(range(len(probability2)),probability2,color="green",label="Binomial p="+str(data[2]))    
    plt.legend(loc=2, bbox_to_anchor=(1.0,1.05),borderaxespad = 0.)
    
def create_data(begin,N,delta):
    data=[]
    for i in np.arange(begin,N,delta) :
        data.append(i)
        data.append(N)
    data=np.reshape(data,(-1,2)).tolist()
    return data
    
for mu,N in create_data(5,100,5):
    display(Poisson_distribution(mu,N),Binomial_distribution(mu/N,N),[mu,N,round(mu/N,2)])
plt.xticks(range(5,100,5))
plt.show()

