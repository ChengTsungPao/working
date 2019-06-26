import numpy as np
import matplotlib.pylab as plt

def Simple_Stirling(N):
    value = (N**N)*np.e**(1-N)
    return value

def Improve_Stirling(N):
    value = (np.e**(-N))*(N**N)*((2*np.pi*N)**0.5)
    return value

def Gosper(N):
    value = (np.e**(-N))*(N**N)*((2*np.pi*N+np.pi/3)**0.5)
    return value

def display(start,end):
    number = range(start,end)
    approximate1=[]
    approximate2=[]
    approximate3=[]
    factorial=[]
    for i in number:
        approximate1.append(Simple_Stirling(i))
        approximate2.append(Improve_Stirling(i))
        approximate3.append(Gosper(i))
        factorial.append(np.math.factorial(i))

    approximate1=np.array(approximate1)
    approximate2=np.array(approximate2)
    approximate3=np.array(approximate3)
    factorial=np.array(factorial)

    plt.subplot(221)
    plt.title("Approximate of N!")
    plt.xlabel("number of N")
    plt.ylabel("value of function")
    plt.plot(number[0:5:1],approximate1[0:5:1],"-o",color="green",label="Simple_Stirling(N)")
    plt.plot(number[0:5:1],approximate2[0:5:1],"-o",color="blue",label="Improve_Stirling(N)")
    plt.plot(number[0:5:1],approximate3[0:5:1],"-o",color="red",label="Gosper(N)")
    plt.plot(number[0:5:1],factorial[0:5:1],"-o",color="black",label="Factorial(N)")
    plt.legend()

    plt.subplot(222)
    plt.title("Error of Simple_Stirling(N)")
    plt.xlabel("number of N")
    plt.ylabel("error of function")
    plt.plot(number,abs(approximate1-factorial)/factorial,"-o",color="green",label="Simple_Stirling(N)")
    plt.legend()

    plt.subplot(223)
    plt.title("Error of Improve_Stirling(N)")
    plt.xlabel("number of N")
    plt.ylabel("error of function")
    plt.plot(number,abs(approximate2-factorial)/factorial,"-o",color="blue",label="Improve_Stirling(N)")
    plt.legend()

    plt.subplot(224)
    plt.title("Error of Gosper(N)")
    plt.xlabel("number of N")
    plt.ylabel("error of function")
    plt.plot(number,abs(approximate3-factorial)/factorial,"-o",color="red",label="Gosper(N)")
    plt.legend()
    plt.tight_layout()
    plt.show()
    
display(0,30)
