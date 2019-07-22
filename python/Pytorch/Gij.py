import numpy as np
from scipy.integrate import dblquad
from numba import jit
import time

@jit
def eps(kx,ky,mu):
    value = np.cos(kx)+np.cos(ky)+(mu/2.0-2)
    return value

@jit
def R(kx,ky,delta,mu):
    value = eps(kx,ky,mu)**2+(delta**2)*((np.sin(kx))**2+(np.sin(ky))**2)
    return value

def P(kx,ky,start,end):
    value = kx*(end[0]-start[0]) + ky*(end[1]-start[1])
    return value

def ss(kx,ky,start,end):
    value = np.sin(kx*(end[0]-start[0]))*np.sin(ky*(end[1]-start[1]))
    return value    

def sc(kx,ky,start,end):
    value = np.sin(kx*(end[0]-start[0]))*np.cos(ky*(end[1]-start[1]))
    return value

def cs(kx,ky,start,end):
    value = np.cos(kx*(end[0]-start[0]))*np.sin(ky*(end[1]-start[1]))
    return value

def cc(kx,ky,start,end):
    value = np.cos(kx*(end[0]-start[0]))*np.cos(ky*(end[1]-start[1]))
    return value
####################################################################################
def first_Integrate(delta,mu,start,end):
    value = dblquad(lambda kx,ky:np.cos(P(kx,ky,start,end))*eps(kx,ky,mu)/R(kx,ky,delta,mu),
                    -np.pi,
                    np.pi,
                    lambda ky:0,
                    lambda ky:np.pi,
                    )      
    return value[0]/(2*np.pi)**2 

def second_Integrate(delta,mu,start,end):    
    value = dblquad(lambda kx,ky:np.sin(kx)*np.sin(P(kx,ky,start,end))/R(kx,ky,delta,mu),
                    -np.pi,
                    np.pi,
                    lambda ky:0,
                    lambda ky:np.pi,
                    )      
    return delta*value[0]/(2*np.pi)**2 

def third_Integrate(delta,mu,start,end):   
    value = dblquad(lambda kx,ky:np.sin(ky)*np.sin(P(kx,ky,start,end))/R(kx,ky,delta,mu),
                    -np.pi,
                    np.pi,
                    lambda ky:0,
                    lambda ky:np.pi,
                    )      
    return delta*value[0]/(2*np.pi)**2

####################################################################################
def first_Integrate_cc(delta,mu,start,end):
    value = dblquad(lambda kx,ky:cc(kx,ky,start,end)*eps(kx,ky,mu)/R(kx,ky,delta,mu),
                    -np.pi,
                    np.pi,
                    lambda ky:0,
                    lambda ky:np.pi,
                    )      
    return value[0]/(2*np.pi)**2 

def first_Integrate_ss(delta,mu,start,end):
    value = dblquad(lambda kx,ky:ss(kx,ky,start,end)*eps(kx,ky,mu)/R(kx,ky,delta,mu),
                    -np.pi,
                    np.pi,
                    lambda ky:0,
                    lambda ky:np.pi,
                    )      
    return value[0]/(2*np.pi)**2 

def second_Integrate_sc(delta,mu,start,end):    
    value = dblquad(lambda kx,ky:np.sin(kx)*sc(kx,ky,start,end)/R(kx,ky,delta,mu),
                    -np.pi,
                    np.pi,
                    lambda ky:0,
                    lambda ky:np.pi,
                    )      
    return delta*value[0]/(2*np.pi)**2 

def second_Integrate_cs(delta,mu,start,end):    
    value = dblquad(lambda kx,ky:np.sin(kx)*cs(kx,ky,start,end)/R(kx,ky,delta,mu),
                    -np.pi,
                    np.pi,
                    lambda ky:0,
                    lambda ky:np.pi,
                    )      
    return delta*value[0]/(2*np.pi)**2 

def third_Integrate_sc(delta,mu,start,end):   
    value = dblquad(lambda kx,ky:np.sin(ky)*sc(kx,ky,start,end)/R(kx,ky,delta,mu),
                    -np.pi,
                    np.pi,
                    lambda ky:0,
                    lambda ky:np.pi,
                    )      
    return delta*value[0]/(2*np.pi)**2

def third_Integrate_cs(delta,mu,start,end):   
    value = dblquad(lambda kx,ky:np.sin(ky)*cs(kx,ky,start,end)/R(kx,ky,delta,mu),
                    -np.pi,
                    np.pi,
                    lambda ky:0,
                    lambda ky:np.pi,
                    )      
    return delta*value[0]/(2*np.pi)**2

####################################################################################
def Gij(delta,mu,size):
    number = size[0]*size[1]
    G = np.zeros((2*number, 2*number), dtype=complex) 
    for i in range(number):
        for j in range(number):
            start = [int(i/size[0]),i%size[0]]
            end = [int(j/size[0]),j%size[0]]
            G[2*i  ,2*j  ] = 1/2 - first_Integrate(delta,mu,start,end)
            G[2*i+1,2*j+1] = 1/2 + first_Integrate(delta,mu,start,end)
            G[2*i+1,2*j  ] = complex(-second_Integrate(delta,mu,start,end), -third_Integrate(delta,mu,start,end))
            G[2*i  ,2*j+1] = complex(second_Integrate(delta,mu,start,end), -third_Integrate(delta,mu,start,end))
    return G

def Gij_optimization(delta,mu,size):
    number = size[0]*size[1]
    G = np.zeros((2*number, 2*number), dtype=complex) 
    first_database_cc = np.zeros((size[0], size[1]),complex)
    first_database_ss = np.zeros((size[0], size[1]),complex)
    second_database_sc = np.zeros((size[0], size[1]),complex)
    second_database_cs = np.zeros((size[0], size[1]),complex)
    third_database_sc = np.zeros((size[0], size[1]),complex)
    third_database_cs = np.zeros((size[0], size[1]),complex)

    start = [0,0]
    for j in range(number):        
        end = [int(j/size[0]),j%size[0]]
        
        firstcc = first_Integrate_cc(delta,mu,start,end)
        firstss = first_Integrate_ss(delta,mu,start,end)
        secondsc = second_Integrate_sc(delta,mu,start,end)
        secondcs = second_Integrate_cs(delta,mu,start,end)
        thirdsc = third_Integrate_sc(delta,mu,start,end)
        thirdcs = third_Integrate_cs(delta,mu,start,end)
        
        first_database_cc[int(j/size[0]),j%size[0]] = firstcc
        first_database_ss[int(j/size[0]),j%size[0]] = firstss
        second_database_sc[int(j/size[0]),j%size[0]] = secondsc
        second_database_cs[int(j/size[0]),j%size[0]] = secondcs
        third_database_sc[int(j/size[0]),j%size[0]] = thirdsc
        third_database_cs[int(j/size[0]),j%size[0]] = thirdcs

        first = firstcc - firstss
        second = secondsc + secondcs
        third = thirdsc + thirdcs

        G[2*0  ,2*j  ] = 1/2 - first
        G[2*0+1,2*j+1] = 1/2 + first
        G[2*0+1,2*j  ] = complex(-second, -third)
        G[2*0  ,2*j+1] = complex(second, -third)
    
    for i in range(1,number):
        for j in range(number):
            vector = [int(j/size[0])-int(i/size[0]),j%size[0]-i%size[0]]
            c1 = [1,1]
            c2 = [1,1]
            if(vector[0]*vector[1]<0):
                c1[1] = -1                

            if(vector[0]<=0 and vector[1]>=0): 
                c2[0] = -1
                vector = np.abs(vector)
            elif(vector[0]<=0 and vector[1]>=0): 
                c2[1] = -1
                vector = np.abs(vector)
            elif(vector[0]<=0 and vector[1]>=0): 
                c1[0] = -1
                c2[1] = -1
                vector = np.abs(vector)

            firstcc = first_database_cc[vector[0],vector[1]]
            firstss = first_database_ss[vector[0],vector[1]]
            secondsc = second_database_sc[vector[0],vector[1]]
            secondcs = second_database_cs[vector[0],vector[1]]
            thirdsc = third_database_sc[vector[0],vector[1]]
            thirdcs = third_database_cs[vector[0],vector[1]]

            first = c1[0]*firstcc - c1[1]*firstss
            second = c2[0]*secondsc + c2[1]*secondcs
            third = c2[0]*thirdsc + c2[1]*thirdcs

            G[2*i  ,2*j  ] = 1/2 - first
            G[2*i+1,2*j+1] = 1/2 + first
            G[2*i+1,2*j  ] = complex(-second, -third)
            G[2*i  ,2*j+1] = complex(second, -third)
    return G

delta = 0.5
mu = 0.5
size = [2,2]

print("\nGij(delta,mu,size):\n")
t1 = time.perf_counter()
print(Gij(delta,mu,size))
t2 = time.perf_counter()
print("time : "+str(t2-t1))

print("--------------------------------")

print("\nGij_optimization(delta,mu,size):\n")
t1 = time.perf_counter()
print(Gij_optimization(delta,mu,size))
t2 = time.perf_counter()
print("time : "+str(t2-t1))


