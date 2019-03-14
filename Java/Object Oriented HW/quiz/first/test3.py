# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 15:47:24 2019

@author: Cheng
"""

def method(a):
    if a==1:
        print("Move disk 1 from A to C")
    elif a==2:
        print("Move disk 1 from A to B")
        print("Move disk 2 from A to C")
        print("Move disk 1 from B to C")
    elif a==3:
        print("Move disk 1 from A to C")
        print("Move disk 2 from A to B")
        print("Move disk 1 from C to B")
        print("Move disk 3 from A to C")
        print("Move disk 1 from B to A")
        print("Move disk 2 from B to C")
        print("Move disk 1 from A to C")
    
N=int(input("Enter the number of discs : "))
print(" ")
if N<=3:
    method(N)
a=1
for i in range(N-1):
    a=2*a+1

    
print("\nNumber of movement : "+str(a))    





























    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    