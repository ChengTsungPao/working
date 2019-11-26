import numpy as np
from scipy.integrate import dblquad
from numba import jit
import time
import warnings

warnings.filterwarnings('ignore')

@jit
def eps(kx,ky,mu):
    value = 0.5*(np.cos(kx)+np.cos(ky))+(mu/2.0-2*0.5)
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
def f(delta,mu,start,end,kx,ky):
    value = cc(kx,ky,start,end)*eps(kx,ky,mu)/R(kx,ky,delta,mu)
    return value

@jit
def s(delta,mu,start,end,kx,ky):
    value = np.sin(kx)*sc(kx,ky,start,end)/R(kx,ky,delta,mu)
    return value

@jit
def t(delta,mu,start,end,kx,ky):
    value = np.sin(ky)*cs(kx,ky,start,end)/R(kx,ky,delta,mu)
    return value

@jit
def I(m,n):
    if(m==0 and n==0):
        value = 1
    else:
        value = 0
    return value  

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

def first_Integrate(delta,mu,start,end,N):    
    value = gaussxwint_double(lambda kx,ky:f(delta,mu,start,end,kx,ky),0,np.pi,N)   
    return value/(2*(np.pi)**2)

def second_Integrate(delta,mu,start,end,N):    
    value = gaussxwint_double(lambda kx,ky:s(delta,mu,start,end,kx,ky),0,np.pi,N)       
    return delta*value/(2*(np.pi)**2)

def third_Integrate(delta,mu,start,end,N):   
    value = gaussxwint_double(lambda kx,ky:t(delta,mu,start,end,kx,ky),0,np.pi,N)     
    return delta*value/(2*(np.pi)**2)

def Gij(delta,mu,size,N):
    number = size[0]*size[1]
    G = np.zeros((2*number, 2*number), dtype=complex) 
    for i in range(number):
        for j in range(number):
            start = [int(i/size[0]),i%size[0]]
            end = [int(j/size[0]),j%size[0]]
            k = I(end[0]-start[0],end[1]-start[1])
            G[2*i  ,2*j  ] = k/2 - first_Integrate(delta,mu,start,end,N)
            G[2*i+1,2*j+1] = k/2 + first_Integrate(delta,mu,start,end,N)
            G[2*i  ,2*j+1] = complex(-second_Integrate(delta,mu,start,end,N), -third_Integrate(delta,mu,start,end,N))
            G[2*i+1,2*j  ] = complex(second_Integrate(delta,mu,start,end,N), -third_Integrate(delta,mu,start,end,N))
    return G

def Gij_optimization(delta,mu,size,N):
    number = size[0]*size[1]
    G = np.zeros((2*number, 2*number), dtype=complex) 
    first_database = np.zeros((size[0], size[1]),complex)
    second_database = np.zeros((size[0], size[1]),complex)
    third_database = np.zeros((size[0], size[1]),complex)

    start = [0,0]
    for j in range(number):        
        end = [int(j/size[0]),j%size[0]]
        
        first = first_Integrate(delta,mu,start,end,N)
        second = second_Integrate(delta,mu,start,end,N)
        third = third_Integrate(delta,mu,start,end,N)
        
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

N = 100
delta = 1
mu = 1
size = [2,2]

print("\nGij(delta,mu,size):\n")
t1 = time.perf_counter()
print(Gij(delta,mu,size,N))
t2 = time.perf_counter()
print("time : "+str(t2-t1))

print("--------------------------------")

print("\nGij_optimization(delta,mu,size):\n")
t1 = time.perf_counter()
print(Gij_optimization(delta,mu,size,N))
t2 = time.perf_counter()
print("time : "+str(t2-t1))

