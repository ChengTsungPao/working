import time,random
import numpy as np
from math import factorial
import matplotlib.pylab as plt

def dise(trials,N,p):
    histogram = np.zeros(N+1 , int)
    sum = 0.0
    j=0
    r=0
    while j < trials :
        sum = 0
        for i in range(N):
            rd=random.random()
            if(rd<p):
                sum+=1
        histogram[sum] = histogram[sum] + 1
        j=j+1
    probability=histogram/float(np.sum(histogram))    
    return probability

def mean(probability):
    sum=0.
    for i in range(len(probability)):
        sum+=i*probability[i]        
    return sum

def var(probability):
    sum=0.   
    m=mean(probability)
    for i in range(len(probability)):
        sum+=((i-m)**2)*probability[i]        
    return sum

def Gaussian(n,N,p):
    value = 1.0/(2*np.pi*p*(1-p)*N)**0.5
    value = value*np.e**(-((n-p*N)**2)/(2*p*(1-p)*N))
    return value

def predict(N,p):

    def Gaussian_probability(N,p):
        probability=np.zeros(N+1,float)
        for i in range(N+1):
            probability[i]=Gaussian(i,N,p)
        return probability

    probability=Gaussian_probability(N,p)
    m=mean(probability)
    v=var(probability)
    return m,v,probability


print("question one,two,three:\n")
trials = 100000
example=[[10,0.5],[30,0.85],[150,0.03]]
times=0
for N,p in example:    
    prediction=predict(N,p)
    t1=time.clock()
    result=dise(trials,N,p)
    t2=time.clock()
    print("  trials =",trials," number of dise =",N," probability =",p," times =",t2-t1)
    print("  prediction:")
    print("    mean:",prediction[0])
    print("    variance:",prediction[1])
    print("    standard deviation:",(prediction[1])**0.5)
    print("  experiment:")
    print("    mean:",mean(result))
    print("    variance:",var(result))
    print("    standard deviation:",(var(result))**0.5)
    print("  result : experiment results are simlar to prediction answers\n")
    plt.subplot(321+times)
    times+=1
    plt.title("Probability Distribution")
    plt.xlabel("value one times")
    plt.ylabel("probability")
    plt.plot(range(N+1),prediction[2],color="blue",label="experimental")
    plt.plot(range(N+1),result,color="green",label="theoretical")
    plt.legend()
    plt.subplot(321+times)
    times+=1
    plt.title("Deviations of Probability")
    plt.xlabel("value one times")
    plt.ylabel("error of probability")
    plt.plot(range(N+1),abs(result-prediction[2])) 
plt.tight_layout()
plt.show()
