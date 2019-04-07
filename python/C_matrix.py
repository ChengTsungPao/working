# -*- coding: cp950 -*-
import numpy as np
from scipy.integrate import dblquad


def make_C_matrix(DELTA, site_size):
    def eps(Px,Py):
        value = 2*((np.cos(Px))**2+(np.cos(Py))**2)
        return value

    def pow(Px,Py,ri=[0,0],rj=[0,0]):
        value = Px*(ri[0]-rj[0])+Py*(ri[1]-rj[1])
        return value 

    def R(Px,Py,delta):
        value = (eps(Px,Py)**2+4*(delta**2)*((np.sin(Px))**2+(np.sin(Py))**2))**0.5
        return value

    def Cij(delta,mode,ri=[0,0],rj=[0,0]):

        const = 1.0/(4*np.pi**2)
        
        def Nonedeg_real():
            value = dblquad(lambda Px,Py:((-np.cos(pow(Px,Py,ri,rj))*np.sin(Py)
                                          -np.sin(pow(Px,Py,ri,rj))*np.sin(Px))*const
                            *delta/(2.0*R(Px,Py,delta))),
                            0,
                            2*np.pi,
                            lambda Py:0,
                            lambda Py:2*np.pi)  
            return value[0]        
        def Nonedeg_imag():
            value = dblquad(lambda Px,Py:((-np.sin(pow(Px,Py,ri,rj))*np.sin(Py)
                                          +np.cos(pow(Px,Py,ri,rj))*np.sin(Px))*const
                            *delta/(2.0*R(Px,Py,delta))),
                            0,
                            2*np.pi,
                            lambda Py:0,
                            lambda Py:2*np.pi)  
            return value[0]

        
        def leftdeg_real():
            value = dblquad(lambda Px,Py:((-np.cos(pow(Px,Py,ri,rj))*np.sin(Py)
                                          +np.sin(pow(Px,Py,ri,rj))*np.sin(Px))*const
                            *delta/(2.0*R(Px,Py,delta))),
                            0,
                            2*np.pi,
                            lambda Py:0,
                            lambda Py:2*np.pi)  
            return value[0]        
        def leftdeg_imag():
            value = dblquad(lambda Px,Py:((-np.cos(pow(Px,Py,ri,rj))*np.sin(Px)
                                          -np.sin(pow(Px,Py,ri,rj))*np.sin(Py))*const
                            *delta/(2.0*R(Px,Py,delta))),
                            0,
                            2*np.pi,
                            lambda Py:0,
                            lambda Py:2*np.pi)  
            return value[0]

        
        def rightdeg_real():
            value = dblquad(lambda Px,Py:(np.cos(pow(Px,Py,ri,rj))*(1+eps(Px,Py))*const
                            /(2.0*R(Px,Py,delta))),
                            0,
                            2*np.pi,
                            lambda Py:0,
                            lambda Py:2*np.pi)  
            return value[0]
        def rightdeg_imag():
            value = dblquad(lambda Px,Py:(np.sin(pow(Px,Py,ri,rj))*(1+eps(Px,Py))*const
                            /(2.0*R(Px,Py,delta))),
                            0,
                            2*np.pi,
                            lambda Py:0,
                            lambda Py:2*np.pi)  
            return value[0]

        
        def twodeg_real():
            value = dblquad(lambda Px,Py:(np.cos(pow(Px,Py,ri,rj))*(1-eps(Px,Py))*const
                            /(2.0*R(Px,Py,delta))),
                            0,
                            2*np.pi,
                            lambda Py:0,
                            lambda Py:2*np.pi)  
            return value[0]
        def twodeg_imag():
            value = dblquad(lambda Px,Py:(np.sin(pow(Px,Py,ri,rj))*(1-eps(Px,Py))*const
                            /(2.0*R(Px,Py,delta))),
                            0,
                            2*np.pi,
                            lambda Py:0,
                            lambda Py:2*np.pi)  
            return value[0]


        def choose(mode):
            value = {
                0 : complex(Nonedeg_real(),Nonedeg_imag()),
                1 : complex(leftdeg_real(),leftdeg_imag()),
                2 : complex(rightdeg_real(),rightdeg_imag()),
                3 : complex(twodeg_real(),twodeg_imag())
            }   
            return value.get(mode,None)
        
        return choose(mode)

    '''
    print(Cij(DELTA ,0,[2,3],[3,2])) 
    print(Cij(DELTA ,1,[2,3],[3,2]))
    print(Cij(DELTA ,2,[2,3],[3,2]))
    print(Cij(DELTA ,3,[2,3],[3,2]))
    '''
    def make_Cij(DELTA, ri=[0, 0], rj=[0, 0]):
        Cij_cell = [[0, 0], [0, 0]]
        Cij_cell[0][1]= Cij(DELTA ,0,ri,rj)
        Cij_cell[1][1]= Cij(DELTA ,1,ri,rj)
        Cij_cell[0][0]= Cij(DELTA ,2,ri,rj)
        Cij_cell[1][0]= Cij(DELTA ,3,ri,rj)
        return Cij_cell

    total_site = site_size[0]*site_size[1]
    
    C_matrix = np.zeros([total_site*2, total_site*2], dtype=complex)
    for i in range(total_site):
        for j in range(total_site):
            ri = [i%site_size[1],i/site_size[1]]
            rj = [j%site_size[1],j/site_size[1]]
            print(i, j, ri, rj)
            Cij_cell = make_Cij(DELTA, ri, rj)
            for a in range(2):
                for b in range(2):
                    C_matrix[i*2+a, j*2+b] = Cij_cell[a][b]
    return C_matrix


DELTA = 4
site_size = (2, 2)
A = make_C_matrix(DELTA, site_size)

        
    
    
    


        





