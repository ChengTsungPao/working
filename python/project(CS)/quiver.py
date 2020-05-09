import matplotlib.pyplot as plt
import numpy as np

X, Y = np.meshgrid(np.arange(0, 6, .2), np.arange(0, 6, .2))

r = 3
U = (X-r)**2#np.cos(X)
V = (Y-r)**2#np.sin(Y)

plt.title('gradient')
plt.quiver(X, Y, U, V, units='width')
plt.show()
