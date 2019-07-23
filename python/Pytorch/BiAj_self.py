import copy
import numpy as np
from scipy.integrate import romberg
from numba import jit
import time

@jit
def eps(kx,ky,mu):
    value = np.cos(kx)+np.cos(ky)+(mu/2.0-2)
    return value

@jit
def R(kx,ky,delta,mu):
    value = (eps(kx,ky,mu)**2+(delta**2)*((np.sin(kx))**2+(np.sin(ky))**2))**0.5
    return value

@jit
def f(delta,mu,start,end,kx,ky):
    value = eps(kx,ky,mu)*(np.cos(kx*(end[0]-start[0]))*np.cos(ky*(end[1]-start[1])))/R(kx,ky,delta,mu)                                 
    return value

@jit
def s(delta,mu,start,end,kx,ky):
    value = delta*np.sin(kx)*np.sin(kx*(end[0]-start[0]))*np.cos(ky*(end[1]-start[1]))/R(kx,ky,delta,mu)                              
    return value

def double_Integrate(f,delta,mu,start,end,N):
    a = np.linspace(0,np.pi,N)
    A1 = romberg(lambda ky:f(delta,mu,start,end,0,ky),0,np.pi)
    vol = 0
    for i in range(1,len(a)):
        A2 = romberg(lambda ky:f(delta,mu,start,end,a[i],ky),0,np.pi)
        A = (A1+A2)/2.0
        vol = vol + A*np.pi/(len(a)-1)
        A1 = A2
    return -vol/(np.pi)**2

def BiAj(delta,mu,size,N):
    number = size[0]*size[1]
    BA = np.zeros((number, number),float)    
    for i in range(number):
        for j in range(number):
            start = [int(i/size[0]),i%size[0]]
            end = [int(j/size[0]),j%size[0]]
            BA[i,j] = double_Integrate(f,delta,mu,start,end,N) + double_Integrate(s,delta,mu,start,end,N)
    return BA

def BiAj_optimization(delta,mu,size,N):
    number = size[0]*size[1]
    first_database = np.zeros((size[0], size[1]),float)
    second_database = np.zeros((size[0], size[1]),float)
    BA = np.zeros((number, number),float)

    start = [0,0]
    for j in range(number):        
        end = [int(j/size[0]),j%size[0]]
        first_database[int(j/size[0]),j%size[0]] = double_Integrate(f,delta,mu,start,end,N)
        second_database[int(j/size[0]),j%size[0]] = double_Integrate(s,delta,mu,start,end,N)
        BA[0,j] = first_database[int(j/size[0]),j%size[0]] + second_database[int(j/size[0]),j%size[0]]       

    for i in range(1,number):
        for j in range(number):
            c = 1
            vector = [int(j/size[0])-int(i/size[0]),j%size[0]-i%size[0]]
            vector[1] = abs(vector[1])
            if(vector[0] < 0):
                c = -1
                vector[0] = abs(vector[0])
            BA[i,j] = first_database[vector[0],vector[1]] + c*second_database[vector[0],vector[1]]
    return BA

N = 1000
delta = 0.5
mu = 0.5
size = [2,2]

print("\nBiAj(delta,mu,size):\n")
t1 = time.perf_counter()
print(BiAj(delta,mu,size,N))
t2 = time.perf_counter()
print("time : "+str(t2-t1))

print("--------------------------------")

print("\nBiAj_optimization(delta,mu,size):\n")
t1 = time.perf_counter()
print(BiAj_optimization(delta,mu,size,N))
t2 = time.perf_counter()
print("time : "+str(t2-t1))








