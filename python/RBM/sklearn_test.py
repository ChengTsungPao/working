import numpy as np
import matplotlib.pyplot as plt


import pandas as pd
path = "D:/program/vscode_workspace/private/data/project_RBM(phy)/"
def gen_mnist_image(X):
    return np.rollaxis(np.rollaxis(X[0:200].reshape(20, -1, 28, 28), 0, 2), 1, 3).reshape(-1, 20 * 28)
X_train = pd.read_csv(path+'train.csv').values[:,1:]
print(X_train)
X_train = (X_train - np.min(X_train, 0)) / (np.max(X_train, 0) + 0.0001)  # 0-1 scaling
#plt.figure(figsize=(10,20))
#plt.imshow(gen_mnist_image(X_train))