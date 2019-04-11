# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 00:35:14 2019

@author: 鄭琮寶
"""
import numpy as np
import time,random
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

def mean(histogram,N):
    sum=0.
    trials=0.
    for i in range(len(histogram)):
        sum+=(i+N)*histogram[i]
        trials+=histogram[i]
    return float(sum)/float(trials)

def var(histogram,N):
    sum=0.
    trials=0.
    m=mean(histogram,N)
    for i in range(len(histogram)):
        sum+=((i+N-m)**2)*histogram[i]
        trials+=histogram[i]
    return float(sum)/float(trials)

def mul(data,sides):
    ans = np.zeros(len(data)+sides-1 , int)
    for i in range(sides):
        for j in range(len(data)):
            ans[i+j] = ans[i+j] + data[j]
    return ans

def predict(sides,trials,N):
    times = np.ones(sides , int)
    for i in range(N-1):
        times = mul(times,sides)
    sum=0.
    for i in range(sides*N-N+1):
        sum+=(i+N)*times[i]
    m=float(sum)/float(sides**N)
    sum=0.
    for i in range(sides*N-N+1):
        sum+=((i+N-m)**2)*times[i]
    v=float(sum)/float(sides**N)
    return m,v

def pos(result):
    maximum=result[0]    
    maxpos=0
    for i in range(len(result)):
        if(maximum<result[i]):
            maximum=result[i]
            maxpos=i
    halfmaxpos=[0,0]
    halfmax=abs(result[0]-np.max(result)/2)
    for i in range(maxpos):
        if(halfmax>abs(result[i]-np.max(result)/2)):
            halfmax=abs(result[i]-np.max(result)/2)
            halfmaxpos[0]=i
    halfmax=abs(result[maxpos]-np.max(result)/2)
    for i in range(maxpos,len(result)):
        if(halfmax>abs(result[i]-np.max(result)/2)):
            halfmax=abs(result[i]-np.max(result)/2)
            halfmaxpos[1]=i
    return maxpos,halfmaxpos

############################question one and two##################################
print "question one and two:\n"

print "question (a):"
N = 2
sides = 10;
trials = 500000;
prediction1=predict(sides,trials,N)
t1=time.clock()
result1=dise(sides,trials,N)
t2=time.clock()
print "  sides =",sides," trials =",trials," number of dise =",N," times =",t2-t1
print "  prediction:"
print "    mean:",prediction1[0]
print "    variance:",prediction1[1]
print "    standard deviation:",(prediction1[1])**0.5
print "  experiment:"
print "    mean:",mean(result1,N)
print "    variance:",var(result1,N)
print "    standard deviation:",(var(result1,N))**0.5
print "  result : experiment results are simlar to prediction answers\n"

print "question (b):"
N = 2
sides = 20;
trials = 500000;
prediction2=predict(sides,trials,N)
t1=time.clock()
result2=dise(sides,trials,N)
t2=time.clock()
print "  sides =",sides," trials =",trials," number of dise =",N," times =",t2-t1
print "  prediction:"
print "    mean:",prediction2[0]
print "    variance:",prediction2[1]
print "    standard deviation:",(prediction2[1])**0.5
print "  experiment:"
print "    mean:",mean(result2,N)
print "    variance:",var(result2,N)
print "    standard deviation:",(var(result2,N))**0.5
print "  result : experiment results are simlar to prediction answers"
print "--------------------------------------------------------------------------------"

################################question three#####################################
print "question three:\n"

N = 5
sides = 10;
trials = 500000;
prediction1=predict(sides,trials,N)
t1=time.clock()
result1=dise(sides,trials,N)
t2=time.clock()
print "sides =",sides," trials =",trials," number of dise =",N," times =",t2-t1
print "prediction:"
print "  width of the distribution:",2.355*((prediction1[1])**0.5)
print "experiment:"
print "  width of the distribution:",abs(pos(result1)[1][0]-pos(result1)[1][1])
print "result : experiment results are simlar to prediction answers\n"
print "line chart plot in other window"
print "result : width of the distribution decrease with increasing numbers of dice"

data=[]
for i in range(1,30,5):
    result1=dise(sides,trials,i)
    data.append(abs(pos(result1)[1][0]-pos(result1)[1][1])/float(sides*i-i+1))
plt.plot(range(1,30,5),data,"-o")
plt.title("question three")
plt.xlabel("number of dise")
plt.ylabel("width of the distribution")
plt.show()
































