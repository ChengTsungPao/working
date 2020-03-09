import cv2
import copy
import numpy as np
import matplotlib.pyplot as plt
from glob import glob

from sklearn import linear_model, metrics
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
from sklearn.pipeline import Pipeline
from sklearn import svm
import warnings

warnings.filterwarnings('ignore')

def get_data(path):
    health = glob(path+"health/*.bmp")
    unhealth = glob(path+"unhealth/*.bmp")
    filename = health + unhealth
    X = []
    Y = np.array([0. for _ in range(len(health))] + [1. for _ in range(len(unhealth))])
    for f in filename:
        X.append(np.array(cv2.imread(f),float).flatten()/255.)
    X = np.array(X)
    X.reshape(len(health) + len(unhealth), -1)
    return X, Y


path = "D:/program/vscode_workspace/private/data/project_image(CS)/"
X, Y = get_data(path)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=0)
print("number of data:",len(X))

model = linear_model.LogisticRegression()
#model = svm.SVC()
model.fit(X_train, Y_train)

Y_pred = model.predict(X_test)
print("X_test:",X_test)
print("predict:",Y_pred)
print("LogisticRegression:\n%s" % (metrics.classification_report(Y_test, Y_pred)))
print("X_test accuracy: "+str(metrics.accuracy_score(Y_test, Y_pred)))
print("----------------------------------------")

dx = 1
plt.title("LogisticRegression predict:")
print(model.predict(X))
plt.scatter(range(len(X))[::dx],model.predict(X)[::dx])
plt.show()
