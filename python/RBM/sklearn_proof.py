import numpy as np
import matplotlib.pyplot as plt

from scipy.ndimage import convolve
from sklearn import linear_model, datasets, metrics
from sklearn.model_selection import train_test_split
from sklearn.neural_network import BernoulliRBM
from sklearn.pipeline import Pipeline
from sklearn.base import clone
from sklearn.cluster import KMeans
import warnings

warnings.filterwarnings('ignore')

def data():
    path = "D:/program/vscode_workspace/private/data/project_RBM(phy)/"
    filename = "G_eigenvalue_train_L=20_mu=[0,10]_delta=1.npz"
    f = np.load(path+filename)
    return f["arr_0"],f["arr_1"]-1

def test():
    path = "D:/program/vscode_workspace/private/data/project_RBM(phy)/"
    filename = "G_eigenvalue_test_L=20_mu=[0,10]_delta=1.npz"
    f = np.load(path+filename)
    return f["arr_0"],f["arr_1"]-1

X, Y = data()
#X = (X - np.min(X, 0)) / (np.max(X, 0) + 0.0001)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.5, random_state=0)

#########################################################################################################################

rbm = BernoulliRBM(random_state=0, verbose=True)
rbm.learning_rate = 0.06
rbm.n_iter = 10

rbm.n_components = 100
kmeans = KMeans(2)

rbm.fit(X_train)
kmeans.fit(rbm.gibbs(X_test))
print(kmeans.labels_,end=" ")
print(Y_test,end=" ")
print(len(kmeans.labels_),len(Y_test))
print(metrics.accuracy_score(Y_test, kmeans.labels_))

#########################################################################################################################

logistic = KMeans(2)
rbm = BernoulliRBM(random_state=0, verbose=True)
rbm_features_classifier = Pipeline(steps=[('rbm', rbm), ('logistic', logistic)])

rbm.learning_rate = 0.06
rbm.n_iter = 10
rbm.n_components = 100
logistic.C = 6000
rbm_features_classifier.fit(X_train)

Y_pred = rbm_features_classifier.predict(X_test) 
print(Y_pred,end=" ")
print(Y_test,end=" ")
print(len(Y_pred),len(Y_test))
print(metrics.accuracy_score(Y_test, rbm_features_classifier.predict(X_test)))
