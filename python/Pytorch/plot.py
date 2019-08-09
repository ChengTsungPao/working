import numpy as np
import matplotlib.pylab as plt

file = np.load("D:/program/vscode_workspace/private/data/project_train/npzfile/201908071856,phase=[5, 1],N=6,gpu.npz")
print(file["phase1"])
print(file["phase2"])
plt.plot(range(len(file["phase1"])),file["phase1"],"o")
plt.plot(range(len(file["phase2"])),file["phase2"],"o")
plt.show()


