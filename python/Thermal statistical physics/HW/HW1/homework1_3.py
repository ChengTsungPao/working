# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 00:35:14 2019

@author: 鄭琮寶
"""
import numpy as np
import time,random

def dise(sides,trials):
    histogram = np.zeros(sides , int)
    sum = 0.0
    j=0
    r=0
    while j < trials :
        r=int(random.random()*sides)
        histogram[r] = histogram[r] + 1
        j=j+1
    return histogram

def mean(histogram):
    sum=0.
    trials=0.
    for i in range(len(histogram)):
        sum+=(i+1)*histogram[i]
        trials+=histogram[i]
    return float(sum)/float(trials)

def var(histogram):
    sum=0.
    trials=0.
    m=mean(histogram)
    for i in range(len(histogram)):
        sum+=((i+1-m)**2)*histogram[i]
        trials+=histogram[i]
    return float(sum)/float(trials)

def predict(sides,trials):
    sum=0.
    for i in range(sides):
        sum+=(i+1)
    m=float(sum)/float(sides)
    sum=0.
    for i in range(sides):
        sum+=(i+1-m)**2
    v=float(sum)/float(sides)
    return m,v

#################################question one######################################          
print "question one:"
print "write on other window"
print "----------------------------------------------------------------------"

############################question two and three#################################
print "question two and three:\n"      

#data one
sides = 10;
trials = 500000;
prediction1=predict(sides,trials)
t1=time.clock()
result1=dise(sides,trials)
t2=time.clock()
print "sides =",sides," trials =",trials," times =",t2-t1
print "prediction:"
print "  mean:",prediction1[0]
print "  variance:",prediction1[1]
print "  standard deviation:",(prediction1[1])**0.5
print "experiment:"
print "  mean:",mean(result1)
print "  variance:",var(result1)
print "  standard deviation:",(var(result1))**0.5
print "result : experiment results are simlar to prediction answers\n"

#data two
sides = 20;
trials = 500000;
prediction2=predict(sides,trials)
t1=time.clock()
result2=dise(sides,trials)
t2=time.clock()
print "sides =",sides," trials =",trials," times =",t2-t1
print "prediction:"
print "  mean:",prediction2[0]
print "  variance:",prediction2[1]
print "  standard deviation:",(prediction2[1])**0.5
print "experiment:"
print "  mean:",mean(result2)
print "  variance:",var(result2)
print "  standard deviation:",(var(result2))**0.5
print "result : experiment results are simlar to prediction answers"
print "----------------------------------------------------------------------"

#################################question four#####################################
print "question four:\n"

delta=1000
sides = 20;
trials = 0;
err=1;
while(delta>=1):

    flag=0    
    while(flag<10):        
        trials=trials+delta        
        prediction=predict(sides,trials)
        result=dise(sides,trials)
        err=np.max([abs((mean(result)-prediction[0])/prediction[0]),
                    abs((var(result)-prediction[1])/prediction[1]),
                    abs((var(result)**0.5-prediction[1]**0.5)/(prediction[1]**0.5))])
        print "sides =",sides," trials =",trials," error =",str(err*100)+"%"
        if err<=0.01:
            flag+=1
            trials=trials-delta
        else:
            flag=0
        
    print "----------------------------------------change delta"
    trials=trials-delta    
    delta=delta/10
    if (delta>=1): err=1   

print "\nFinal Answer:"
print "sides =",sides," trials =",trials," error =",str(err*100)+"%"
