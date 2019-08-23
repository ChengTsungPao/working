import numpy as np
import matplotlib.pylab as plt

file = np.load("D:/program/vscode_workspace/private/data/project_train/npzfile/201908240217,phase=[5, 1],N=5,gpu.npz")
print(file["phase1"])
print(file["phase2"])
#print(file["phase3"])
#print(file["phase4"])
plt.plot(range(len(file["phase1"])),file["phase1"],"o")
plt.plot(range(len(file["phase2"])),file["phase2"],"o")
#plt.plot(range(len(file["phase3"])),file["phase3"],"o")
#plt.plot(range(len(file["phase4"])),file["phase4"],"o")
plt.show()


