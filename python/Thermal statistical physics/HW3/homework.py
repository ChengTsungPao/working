import numpy as np
import matplotlib.pylab as plt

def Dirac(alpha,x):
    value = np.e**(-(x**2)/(2*alpha**2))/(2*np.pi*alpha)**0.5
    return value

x=np.linspace(-2,2,10000)
alpha=[1,0.1,0.01,0.001]
color=["orange","blue","green","red"]
for i in range(len(alpha)):
    y=[]
    for j in range(len(x)):
        y.append(Dirac(alpha[i],x[j]))
    plt.plot(x,y,color=color[i],label="\u03B1="+str(alpha[i]))
plt.title("\u03B4(x)",fontsize=20)
plt.xlabel("x",fontsize=15)
plt.ylabel("y",fontsize=15)
plt.legend(fontsize=15)
plt.show()
