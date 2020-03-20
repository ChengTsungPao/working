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
    health = np.load(path+"health.npz")["r"]
    unhealth = np.load(path+"unhealth.npz")["r"]
    X = np.array(health.tolist() + unhealth.tolist())
    Y = np.array([0. for _ in range(len(health))] + [1. for _ in range(len(unhealth))])
    return X, Y

path = "./erythrocyte/"
X, Y = get_data(path)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, shuffle=True)
print("number of data:",len(X))

model = linear_model.LogisticRegression()
model = svm.SVC(probability=True)
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
plt.scatter(range(len(X))[::dx],model.predict_proba(X)[::dx,0])
plt.scatter(range(len(X))[::dx],model.predict(X)[::dx])
plt.show()
