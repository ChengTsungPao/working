# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 15:00:13 2017

@author: Cheng
"""
import numpy as np

def trapezoidal(f,a,b,n):#指定間格之函數
   
    N=float(b-a)/float(n)#間隔寬
    total=N*(f(a)+f(b))/2.0#公式的常數項    
    for i in range(1,n):#公式的總和項，利用for疊加
        total=total+f(a+i*N)*N
       
    return total

def etrapezoidal(f,a,b,err):#指定誤差之函數

    x=2
    N=float(b-a)/float(x)
    s1=trapezoidal(f,a,b,1)#1格積分值
    s2=s1/2.0+f(a+1*N)*N#2格積分值
    tuple=s1,s2#建立個有兩個元的tuple
    
    while abs(tuple[1]-tuple[0])/3.0>err:#誤差公式
        
        x=x*2#誤差未達指定範圍後，間格數需乘2
        N=float(b-a)/float(x)#間隔寬
        
        s=tuple[1]/2.0#公式的常數項
        for j in np.arange(1,x,2):#公式的總和項，利用for疊加
            s=s+f(a+j*N)*N
      
        tuple=tuple[1],s#新的項變為此tuple的第一項，舊的第一項變成第零項
                  
    return tuple[1],abs(tuple[1]-tuple[0])/3.0,x
    
def simpson(f,a,b,n):
    N=float(b-a)/float(n)#間距
    s=N*(f(a)+f(b))/3.0#公式常數項
    for i in range(1,n,2):#公式奇數項
        s=s+(4*f(a+i*N))*N/3.0
    for i in range(2,n,2):#公式偶數項
        s=s+(2*f(a+i*N))*N/3.0
    return s
    
def esimpson(f,a,b,err):
    n=2#間格數
    N=float(b-a)/float(n)#第一項間距
    s1=(f(a)+f(b))/3.0#S公式的常數項
    for i in range(2,n,2):#第一個S帶公式
        s1=s1+(2*f(a+i*N))/3.0  
    T1=0#T公式的常數項
    for i in range(1,n,2):#第一個T帶公式
        T1=T1+(2*f(a+i*N))/3.0
    I1=N*(s1+2*T1)#利用S與T推出第一個積分值
    n=n*2#間格數乘2
    N=float(b-a)/float(n)#第二項間距
    s2=s1+T1#利用遞迴關係式推出下一項(第二項)
    T2=0#T公式的常數項
    for i in range(1,n,2):#第二個T帶公式
        T2=T2+(2*f(a+i*N))/3.0
    I2=N*(s2+2*T2)#利用S與T推出第二個積分值
    tuple_s=s1,s2#建立S之tuple
    tuple_T=T1,T2#建立T之tuple
    tuple=I1,I2#建立I之tuple
    while abs(tuple[1]-tuple[0])/15.0>err:#連續判斷誤差是否在給定的值內
        
        n=n*2#間格數乘2
        N=float(b-a)/float(n)#新的間格
        s=tuple_s[1]+tuple_T[1]#利用遞迴關係式推出下一項
        T=0#T公式的常數項
        for i in range(1,n,2):#新T帶公式
            T=T+(2*f(a+i*N))/3.0
        I=N*(s+2*T)#利用S與T推出新的積分值
        tuple_s=tuple_s[1],s#建立新S之tuple
        tuple_T=tuple_T[1],T#建立新T之tuple
        tuple=tuple[1],I#建立新I之tuple        
    return tuple[1],abs(tuple[1]-tuple[0])/15.0,n#回傳定義值
    
def J(m,x):#定義J
    ans=esimpson(lambda a:(np.cos(m*a-x*np.sin(a)))/np.pi,0,np.pi,10**(-6))#利用esimpson計算特定x與m情況下J之積分值
    return ans#回傳定義值

def Romberg_use(i):#定義一個Romberg會用到的函數
                   #例如：Romberg_use([R11,R21,R31])=[[R11,R21,R31],[R22,R32],[R33]]
    I_list=[i]
    for j in range(len(i)-1):#插入需要的list空格數量
        I_list.append([])
    n=0
    while len(I_list[n])>1:#有數字的list[n]數目內大於1，繼續運算
        for j in range(len(I_list[n])-1):#list[n]內要運算的次數
            erri=(I_list[n][j+1]-I_list[n][j])/(float(4**(n+1)-1))#這一列的誤差
            I=I_list[n][j+1]+erri#誤差加原數
            I_list[n+1].append(I)#丟進下一列
        n=n+1
    return I_list

def Romberg_list(f,a,b,err):
    
    I1=trapezoidal(f,a,b,4)#梯形法求積分值
    I2=trapezoidal(f,a,b,8)#梯形法求積分值
    I=[I1,I2]#建立Romberg_use會用到的list
    s=Romberg_use(I)#帶入Romberg_use計算
    n=8
    while abs(s[len(s)-2][1]-s[len(s)-2][0])/float(4**(len(s))-2)>err:#誤差(兩個數那列)
        n=n*2
        newi=trapezoidal(f,a,b,n)#梯形法求積分值
        I.append(newi)#加入I中
        s=Romberg_use(I)#帶入Romberg_use計算
        
    return s    

def Romberg(f,a,b,err):
    
    I1=trapezoidal(f,a,b,4)#梯形法求積分值
    I2=trapezoidal(f,a,b,8)#梯形法求積分值
    I=[I1,I2]#建立Romberg_use會用到的list
    s=Romberg_use(I)#帶入Romberg_use計算
    n=8
    while abs(s[len(s)-2][1]-s[len(s)-2][0])/float(4**(len(s))-2)>err:#誤差(兩個數那列)
        n=n*2
        newi=trapezoidal(f,a,b,n)#梯形法求積分值
        I.append(newi)#加入I中
        s=Romberg_use(I)#帶入Romberg_use計算
        
    return s[len(s)-1][0]


