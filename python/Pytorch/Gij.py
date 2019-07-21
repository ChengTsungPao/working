import numpy as np
from scipy.integrate import dblquad
from numba import jit

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

delta = 0.5
mu = 0.5
size = [2,2]

print(Gij(delta,mu,size))

