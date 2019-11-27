# -*- coding: utf-8 -*-
"""
20190723 BA
"""
from numpy import sin,cos,pi,sum,abs,zeros,arange,transpose
import numpy as np
from scipy.integrate import tplquad,dblquad,quad
from time import perf_counter
from numba import jit
 

#double integral
'''example
val,err = dblquad(lambda y,x : sin(x)*cos(y),#function
                  0,#x_下界0
                  pi,#x_上界pi
                  lambda x:0,#y下界x^2
                  lambda x:pi)#y上界2*x

print ('dblquad：',val)
'''

def gaussxw(N):
    # Initial approximation to roots of the Legendre polynomial
    a = np.linspace(3,4*N-1,N)/(4*N+2)
    x = np.cos(np.pi*a+1/(8*N*N*np.tan(a)))
    # Find roots using Newton's method
    epsilon = 1e-15
    delta = 1.0
    while delta>epsilon:
        p0 = np.ones(N,float)
        p1 = np.copy(x)
        for k in range(1,N):
            p0,p1 = p1,((2*k+1)*x*p1-k*p0)/(k+1)
        dp = (N+1)*(p0-x*p1)/(1-x*x)
        dx = p1/dp
        x -= dx
        delta = max(abs(dx))
    # Calculate the weights
    w = 2*(N+1)*(N+1)/(N*N*(1-x*x)*dp*dp)
    return x,w

def gaussxwint_double(f,a,b,N):
    xp,wp=gaussxw(N)
    xp=0.5*(b-a)*xp+0.5*(b+a)
    wpx=0.5*(b-a)*wp
    yp,wp=gaussxw(N)
    yp=0.5*(b-a)*yp+0.5*(b+a)
    wpy=0.5*(b-a)*wp
    I=0.0
    for i in range (N):
        I += sum(f(xp,yp[i])*wpx*wpy[i])
    return I

def R(x,y):
    return (((cos(x)+cos(y))+(0.5*mu/0.5)-2)**2+(sin(x)**2+sin(y)**2)*(delta**2))**0.5
    

def integral_term1(kx,ky):
    #need mu,delta,d_m,d_n
    term_1 = (1/abs(R(kx,ky)))
    term_2_part1 = ((cos(kx)+cos(ky))+(0.5*mu/0.5)-2)*(cos(kx*d_m)*cos(ky*d_n))
    term_2_part2 = 0
    term_2 = term_2_part1+term_2_part2
    return term_1*term_2


def integral_term2(kx,ky):
    #need mu,delta,d_m,d_n
    term_1 = (1/abs(R(kx,ky)))
    term_2_part1 = 0
    term_2_part2 = delta*sin(kx)*sin(kx*d_m)*cos(ky*d_n)
    term_2 = term_2_part1+term_2_part2
    return term_1*term_2

def BiAj(f,mu,delta,d_m,d_n):
    lower = 0
    upper = pi
    I = gaussxwint_double(f,lower,upper,100)
    biaj = -1*(1/pi**2)*I
    return biaj




#test
'''
#parameter
d_m = 1     #delta_m = m_prime-m
d_n = 1     #delta_n = n_prime-n
mu = 0.5
delta = 0.5

val,err = dblquad(lambda y,x : integral_term(x,y),      #function
                  0,    #x_下界0
                  pi,   #x_上界pi
                  lambda x:0,   #y下界x^2
                  lambda x:pi)  #y上界2*x


print ('dblquad：',-1*(1/pi**2)*val)
print('gaussxwint：',BiAj(mu,delta,d_m,d_n))
'''

def BA(N,mu,delta):     # n is n*n pratical
    NN = N**2 #從邊長算出粒子數
    matrix = zeros((NN,NN)) #建立BA矩陣
    first_database = np.zeros((N, N),float)
    second_database = np.zeros((N, N),float)
    mn = []
    for m in arange(N):
        for n in arange(N):
            mn.append([m,n])
    #print(mn)

    for i in range(1):
        for j in range(NN):
            global d_m 
            d_m = mn[j][0]-mn[i][0]
            global d_n
            d_n = mn[j][1]-mn[i][1]
            #print(i,j)
            tmp1 = BiAj(integral_term1,mu,delta,d_m,d_n)
            tmp2 = BiAj(integral_term2,mu,delta,d_m,d_n)
            first_database[int(j/N),j%N] = tmp1
            second_database[int(j/N),j%N] = tmp2
            matrix[i,j] = tmp1 + tmp2

    for i in range(1,NN):
        for j in arange(NN):             
            d_m = mn[j][0]-mn[i][0]            
            d_n = mn[j][1]-mn[i][1]
            c = 1
            vector = [int(j/N)-int(i/N),j%N-i%N]
            vector[1] = abs(vector[1])
            if(vector[0] < 0):
                c = -1
                vector[0] = abs(vector[0])
            matrix[i,j] = first_database[vector[0],vector[1]] + c*second_database[vector[0],vector[1]]

    return matrix
            

#parameter
n = input("input the size of BiAj: ")
mu = 1
delta = 1
start = perf_counter()
print(BA(int(n),mu,delta))
end = perf_counter()
print('Time = ',end-start)