# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 15:18:56 2019

@author: Cheng
"""


A=int(input("input the A : "))
N=int(input("input the N : "))

for i in range(A):
    for m in range(N):
        for k in range(A-i):
            print(" ",end="")
        for k in range(2*i-1):
            print("*",end="")
        for k in range(A-i):
            print(" ",end="")            
        for k in range(2*A-1):
            print(" ",end="")   
    print("\n")

for j in range((2*A-1)*N*2):
    print("*",end="")
print("\n")
for i in range(A-1,-1,-1):
    for m in range(N):
        for k in range(2*A-1):
            print(" ",end="")        
        for k in range(A-i):
            print(" ",end="")
        for k in range(2*i-1):
            print("*",end="")
        for k in range(A-i):
            print(" ",end="")  
    print("\n")
  