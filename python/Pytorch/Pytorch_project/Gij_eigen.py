import numpy as np
from scipy.integrate import dblquad
from numba import jit
import warnings

warnings.filterwarnings('ignore')

@jit
def eps(kx,ky,mu):
    value = T*(np.cos(kx)+np.cos(ky))+(mu/2.0-2*T)
    return value

@jit
def R(kx,ky,delta,mu):
    value = (eps(kx,ky,mu)**2+(delta**2)*((np.sin(kx))**2+(np.sin(ky))**2))**0.5
    return value

@jit
def sc(kx,ky,start,end):
    value = np.sin(kx*(end[0]-start[0]))*np.cos(ky*(end[1]-start[1]))
    return value

@jit
def cs(kx,ky,start,end):
    value = np.cos(kx*(end[0]-start[0]))*np.sin(ky*(end[1]-start[1]))
    return value

@jit
def cc(kx,ky,start,end):
    value = np.cos(kx*(end[0]-start[0]))*np.cos(ky*(end[1]-start[1]))
    return value

@jit
def f(kx,ky,delta,mu,start,end):
    value = cc(kx,ky,start,end)*eps(kx,ky,mu)/R(kx,ky,delta,mu)
    return value

@jit
def s(kx,ky,delta,mu,start,end):
    value = np.sin(kx)*sc(kx,ky,start,end)/R(kx,ky,delta,mu)
    return value

@jit
def t(kx,ky,delta,mu,start,end):
    value = np.sin(ky)*cs(kx,ky,start,end)/R(kx,ky,delta,mu)
    return value

@jit
def I(m,n):
    if(m==0 and n==0):
        value = 1
    else:
        value = 0
    return value    

def first_Integrate(delta,mu,start,end):
    value = dblquad(f,
                    0,
                    np.pi,
                    lambda ky:0,
                    lambda ky:np.pi,
                    args=(delta,mu,start,end)
                    )      
    return value[0]/(2*(np.pi)**2)

def second_Integrate(delta,mu,start,end):    
    value = dblquad(s,
                    0,
                    np.pi,
                    lambda ky:0,
                    lambda ky:np.pi,
                    args=(delta,mu,start,end)
                    )      
    return delta*value[0]/(2*(np.pi)**2)

def third_Integrate(delta,mu,start,end):   
    value = dblquad(t,
                    0,
                    np.pi,
                    lambda ky:0,
                    lambda ky:np.pi,
                    args=(delta,mu,start,end)
                    )      
    return delta*value[0]/(2*(np.pi)**2)

def Gij(delta,mu,size):
    number = size[0]*size[1]
    G = np.zeros((2*number, 2*number), dtype=complex) 
    first_database = np.zeros((size[0], size[1]),complex)
    second_database = np.zeros((size[0], size[1]),complex)
    third_database = np.zeros((size[0], size[1]),complex)

    start = [0,0]
    for j in range(number):        
        end = [int(j/size[0]),j%size[0]]
        
        first = first_Integrate(delta,mu,start,end)
        second = second_Integrate(delta,mu,start,end)
        third = third_Integrate(delta,mu,start,end)
        
        first_database[int(j/size[0]),j%size[0]] = first
        second_database[int(j/size[0]),j%size[0]] = second
        third_database[int(j/size[0]),j%size[0]] = third

        k = I(j//size[0]-0,j%size[0]-0)
        G[2*0  ,2*j  ] = k/2 - first
        G[2*0+1,2*j+1] = k/2 + first
        G[2*0  ,2*j+1] = complex(-second, -third)
        G[2*0+1,2*j  ] = complex(second, -third)
    
    for i in range(1,number):
        for j in range(number):
            vector = [int(j/size[0])-int(i/size[0]),j%size[0]-i%size[0]]
            c = [1,1]

            if(vector[0]<0): c[0] = -1
            if(vector[1]<0): c[1] = -1

            vector = np.abs(vector)

            first = first_database[vector[0],vector[1]]
            second = second_database[vector[0],vector[1]]
            third = third_database[vector[0],vector[1]]

            k = I(j//size[0]-i//size[0],j%size[0]-i%size[0])
            G[2*i  ,2*j  ] = k/2 - first
            G[2*i+1,2*j+1] = k/2 + first
            G[2*i  ,2*j+1] = complex(-c[0]*second, -c[1]*third)
            G[2*i+1,2*j  ] = complex(c[0]*second, -c[1]*third)
    return G

def Gij_eigen(delta,mu,size):
    return np.linalg.eigh(Gij(delta,mu,size))

T = 0.5
delta = 1
mu = 1
size = [2,2]

print("\nGij:\n")
print(Gij(delta,mu,size))

eigen = Gij_eigen(delta,mu,size)
print("\neigenvalue:\n")
print(eigen[0])

print("\neigenmatrix:\n")
print(eigen[1])
