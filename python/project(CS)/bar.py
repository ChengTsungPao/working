import matplotlib.pylab as plt
import numpy as np

x = np.arange(0,1,0.1)
y = [0, 0, 0, 0, 0, 0, 29, 369, 567, 35]
plt.title("label")
plt.bar(x, y, width = 0.05)
plt.plot(x, y, "g")
plt.xticks(x)
plt.xlabel("accuracy")
plt.ylabel("times")
plt.show()

x = np.arange(0,1,0.1)
y = [0, 0, 0, 0, 0, 2, 64, 552, 374, 8]
plt.title("radius")
plt.bar(x, y, width = 0.05)
plt.plot(x, y, "g")
plt.xticks(x)
plt.xlabel("accuracy")
plt.ylabel("times")
plt.show()