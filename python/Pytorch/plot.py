import numpy as np
import matplotlib.pylab as plt

file = np.load("D:/program/vscode_workspace/private/data/project_train/npzfile/201908090300,phase=[3, 7],N=5,gpu.npz")
print(file["phase1"])
plt.plot(range(len(file["phase1"])),file["phase1"],"o")
plt.plot(range(len(file["phase2"])),file["phase2"],"o")
plt.show()


