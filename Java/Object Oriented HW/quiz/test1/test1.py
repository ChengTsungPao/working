# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 14:42:36 2019

@author: Cheng
"""


data1="abcdefghijklmnopqrstuvwxyz"

data2="ABCDEFGHIJKLMNOPQRSTUVWXYZ"

data=[data1,data2]

a=input("input the string : ")
num=0
for i in range(len(data1)):
    for j in range(len(a)):
        if data[0][i]==a[j]:
            num=num+1
            break
        elif data[1][i]==a[j]:
            num=num+1
            break
    
print(num)       

