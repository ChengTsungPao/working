# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 00:35:14 2019

@author: 鄭琮寶
"""
import random
from numpy import zeros
from time import clock,time
import matplotlib.pylab as plt

############################question one and two####################################
print "question one and two\n"
trials = 100
print "Number of trials = ", trials 
sides = 6

histogram = zeros(sides , int)
sum = 0.0
j=0
r=0
while j < trials :
    r=int(random.random()*sides)
    histogram[r] = histogram[r] + 1
    j=j+1
j=0
while j < sides :
    print "number of dise :",j+1
    print "  times :",histogram[j],"times deviation :",abs(histogram[j]-trials/sides)
    print "  probability :",histogram[j]/float(trials),"probability deviation :",abs(histogram[j]/float(trials)-1./sides)
    j=j+1

plt.subplot(221)
plt.title("times")
plt.xlabel("dise number")
plt.ylabel("times")
plt.bar(range(sides),histogram,align='center',width=1,color="green")

plt.subplot(222)
plt.title("times deviation")
plt.xlabel("dise number")
plt.ylabel("times")
plt.bar(range(sides),abs(histogram-trials/sides),align='center',width=1,color="cyan")

plt.subplot(223)
plt.title("probability")
plt.xlabel("dise number")
plt.ylabel("probability")
plt.bar(range(sides),histogram/float(trials),align='center',width=1,color="red")

plt.subplot(224)
plt.title("probability deviation")
plt.xlabel("dise number")
plt.ylabel("probability")
plt.bar(range(sides),abs(histogram/float(trials)-1./sides),align='center',width=1,color="white")
plt.tight_layout()
plt.show()
print "\n==============================================================="

#########################question three,four and five################################
print "question three:\n"
delta=10000
trials = 10
datax=[]
data1=[[],[],[],[],[],[]]
data2=[[],[],[],[],[],[]]
while(delta>=10):
    
    while(1==1):
        
        t1=clock()
        trials=trials+delta
        sides = 6
        histogram = zeros(sides,int)
        sum = 0.0
        j = 0
        r = 0
        while j<trials:
            r=int(random.random()*sides)
            histogram[r] = histogram[r] + 1
            j=j+1
        t2=clock()

        if t2-t1>=1:
            break;
        else:
            t=t2-t1
            datax.append(trials)
            for i in range(6):                
                data1[i].append(abs(histogram-trials/sides)[i])
                data2[i].append(abs(histogram/float(trials)-1./sides)[i])
        print "Number of trials =",trials
        print "  times of distribution :",histogram
        print "  time :",t2-t1
        
    print "----------------------------------------change delta"
    trials=trials-delta
    delta=delta/10
    
print "Final Answer:"
print "Number of trials = ",trials," (minimum unit:10)"
print "  times of distribution :",histogram
print "  times deviation of distribution :",abs(histogram - trials/sides)
print "  probability of distribution :",histogram/float(trials)
print "  probability deviation of distribution :",abs(histogram/float(trials)-1./sides)
print "time:",t
print "\n==============================================================="

print "question four:\n"
print "plot on the other window"
print "result : Meaningless because of the trials"
num=["one","two","three","four","five","six"]
for i in range(6):    
    plt.plot(datax,data1[i],"-",label=num[i])
plt.title("the deviation of this number")
plt.xlabel("trials")
plt.ylabel("times")
plt.legend()
plt.show()
print "\n==============================================================="

print "question five:\n"
print "plot on the other window"
print "result : the ratio of the number of times approach closer to 1/6\n"
for i in range(6):    
    plt.plot(datax,data2[i],"-",label=num[i])
plt.title("the probability deviation of this number")
plt.xlabel("trials")
plt.ylabel("probability")
plt.legend()
plt.show()
  
