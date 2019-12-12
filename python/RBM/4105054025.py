# -*- coding: utf-8 -*-
"""
Created on Mon Jan 08 19:57:14 2018

@author: Cheng
"""
from gaussxw import gaussxw
import numpy as np
import matplotlib.pyplot as plt 
import warnings

warnings.filterwarnings('ignore')

def gaussxwint(f,a,b,n):#高斯積分定義
    
    x=gaussxw(n)[0]#原x根的位置
    w=gaussxw(n)[1]#原權重的位置
    
    I=0
    for i in range(len(x)):
        p1=float(b-a)*x[i]/2.0+float(b+a)/2.0#x變數變換
        p2=float(b-a)*w[i]/2.0#w變數變換
        I=I+p2*f(p1)#權重乘函數值相加
        
    return I

def H(n,x):#H(x)函數定義
    h=1,2*x#將前兩項建立成tuple
    for i in range(2,n+1,1):#帶幾次公式
        new=2*x*h[1]-2*(i-1)*h[0]#公式
        h=h[1],new
    y=h[1]
    if n==0:y=h[0]#若n為零直接拿h[0]
    return y

def Nfunction(n):#定義階層函數
    s=1
    for i in range(n,1,-1):#階層公式
        s=s*i#乘上下一項
    return s 
    
def Y(n,x):
    s1=1.0/((2**n)*Nfunction(n)*((np.pi)**0.5))**0.5
    s2=np.e**(-x**2/2.0)
    s3=H(n,x)
    y=s1*s2*s3#題目的積分公式
    return y
    
def root_mean_square(n,N):#<x^2>開根號之定義
    ans=gaussxwint(lambda a:((np.tan(a))**2)*(Y(n,np.tan(a))**2)*(1+(np.tan(a))**2),-np.pi/2.0,np.pi/2.0,N) 
    return ans**(0.5)

def F(z,N):#力的雙重積分之定義
    L=10.0
    y=np.linspace(-L/2.0,L/2.0,N+1)#y方向等分
    h=float(L)/(N)#間格
    s=0
    for i in range(len(y)-1):#帶入積分公式
        s=s+h*gaussxwint(lambda x:(x**2+y[i]**2+z**2)**(-1.5),-L/2.0,L/2,N)#y為某一層之面積大小乘上厚度h
    constant=(6.674*10**(-11))*(100.0/100.0)*z#積分式外的係數
    s=s*constant
    return s

#三個圖一起顯示大約需等待2分鐘
#第一題
print ("第一題")

print ("(a) show in other window")
a=np.linspace(-4,4,100)
for n in range(4):
    b=[]
    for i in a:
        b.append(Y(n,i))
    plt.subplot(221)
    plt.plot(a,b,label="n="+str(n))
    plt.title("Question 1 (a)---H(n,x)")
    plt.legend(loc=4)

print ("(b) show in other window")
c=np.linspace(-10,10,1000)
d=[]
for i in c:
    d.append(Y(30,i))    
plt.subplot(222)
plt.plot(c,d,label="n=30")
plt.title("Question 1 (b)---Y(n,x)")
plt.legend(loc=4)

print ("(c) "+str(root_mean_square(5,100)))

#第二題
print ("第二題")

print ("(a) show in the paper")

print ("(b) show in other window")
N=100
a=np.linspace(0,10,N)
b=[]
for i in a:
    b.append(F(i,N))
plt.subplot(223)
plt.plot(a,b)
plt.title("Question 2 (b)---F(z)")
plt.show()

print ("(c) show in the paper")  
