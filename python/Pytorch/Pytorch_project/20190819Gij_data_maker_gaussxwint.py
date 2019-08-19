import numpy as np
from numba import jit
import numpy as np
from numba import jit
from numpy import sin,cos,pi,sum,abs,zeros,arange,transpose,where,linspace,tan,ones,copy,savez
from scipy.integrate import tplquad,dblquad,quad
from matplotlib.pyplot import imshow,show
from time import localtime,strftime
import os

@jit
def eps(kx,ky,mu):
    value = np.cos(kx)+np.cos(ky)+(mu/2.0-2)
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

        G[2*0  ,2*j  ] = 1/2 - first
        G[2*0+1,2*j+1] = 1/2 + first
        G[2*0+1,2*j  ] = complex(-second, -third)
        G[2*0  ,2*j+1] = complex(second, -third)
    
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

            G[2*i  ,2*j  ] = 1/2 - first
            G[2*i+1,2*j+1] = 1/2 + first
            G[2*i+1,2*j  ] = complex(-c[0]*second, -c[1]*third)
            G[2*i  ,2*j+1] = complex(c[0]*second, -c[1]*third)
    return G

#data output test
"""
mu = 0.5
delta = 0.5
N = 2
Number_of_cuts = 100

data = Gij(delta,mu,[int(N),int(N)],Number_of_cuts)

# 創建存資料的路徑
train_path = "../data/train/"
if not os.path.exists(train_path):
    os.makedirs(train_path)
    
test_path = "../data/test/"
if not os.path.exists(test_path):
    os.makedirs(test_path)

#創建日期標籤
date = strftime("%Y%m%d",localtime()) 

file_name = "{},Gij_matrix,N={},delta={}".format(date,N,delta)
savez(train_path+file_name, data = data, delta=delta, mu=mu)

#load example
'''
A = np.load('filename')
B = A.files
C = A['data']
'''
"""

Number_of_cuts = 100 #切割數

#def 相態根據輸入mu,delta給出當下相態
def phase(delta,mu):
	if delta > 0:
		if mu < 0:
			p = 5
		elif mu < 2:
			p = 1
		elif mu < 4:
			p = 3
		else:
			p = 7
	else:
		if mu < 0:
			p = 6
		elif mu < 2:
			p = 3
		elif mu < 4:
			p = 4
		else:
			p = 8
	return p

#def 訓練用的資料
def train_data_maker(N, delta, mu_point_list, Dir=".\\"):

    Gij_list, phase_label = [],[]
    mu_list = []
    #創建放此三資料矩陣

    delta = delta

    for point in mu_point_list:
    	mu_list.extend(linspace(point,point+0.005,1000))
    #將輸入的mu點延伸為我們要資料的數量
    ##向右延伸0.005切1000格

    count = 0.
    total = float(len(mu_list))
    #完成度計算器

    global mu
    #此處將mu設為全域變數以超出函數範圍使用

    for mu in mu_list:
    	#對於每個mu跑Gij矩陣並將矩陣及相態存入對應list
        Gij_list.append(Gij(delta,mu,[int(N),int(N)],Number_of_cuts))
        phase_label.append(phase(delta,mu) )
        count += 1
        print((count/total)*100.,'%')
        #印出當下完成度
    
    #創建日期標籤
    date = strftime("%Y%m%d", localtime())

    #將list存成npz檔
    file_name = "{},Gij_matrix_train,N={},delta={}".format(date,N,delta)
    savez(Dir+file_name, Gij=Gij_list, phase=phase_label, delta=delta, mu=mu_list)
    
    print('train data save done, filename is : ',file_name)

    return None

#def 測試用的資料
def test_data_maker(N, delta, Dir=".\\"):

    Gij_list, phase_label = [],[]
    mu_list = []
    #創建放此三資料矩陣

    delta = delta

    mu_list.extend(linspace(-10,10,4000))
    #創建mu list,將-10到10切4000點

    count = 0.
    total = float(len(mu_list))
    #完成度計算器

    global mu
	#此處將mu設為全域變數以超出函數範圍使用

    for mu in mu_list:
    	#對於每個mu跑Gij矩陣並將矩陣及相態存入對應list
        Gij_list.append(Gij(delta,mu,[int(N),int(N)],Number_of_cuts))
        phase_label.append(phase(delta,mu) )
        count += 1
        print((count/total)*100.,'%')
        #印出當下完成度
    
    #創建日期標籤
    date = strftime("%Y%m%d", localtime())

    #將list存成npz檔
    file_name = "{},Gij_matrix_test,N={},delta={}".format(date,N,delta)
    savez(Dir+file_name, Gij=Gij_list, phase=phase_label, delta=delta, mu=mu_list)
    
    print('test data save done, filename is : ',file_name)

    return None

# 創建存資料的路徑
train_path = "../data/train/"
if not os.path.exists(train_path):
    os.makedirs(train_path)
    
test_path = "../data/test/"
if not os.path.exists(test_path):
    os.makedirs(test_path)


delta = 1
N = 2

train_data_maker(N, delta, [-1,1,3,5], Dir = train_path)
test_data_maker(N, delta, Dir = test_path)

