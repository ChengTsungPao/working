import numpy as np
import matplotlib.pyplot as plt

from sklearn import linear_model, datasets, metrics
from sklearn.model_selection import train_test_split
from sklearn.neural_network import BernoulliRBM
from sklearn.pipeline import Pipeline
from sklearn.base import clone
from sklearn.cluster import KMeans
import warnings

warnings.filterwarnings('ignore')

# #############################################################################
# Setting up

def data():

    path = "D:/program/vscode_workspace/private/data/project_RBM(phy)/"
    filename = "BA_matrix_train,L=10,mu=[0,3],delta=1.npz"
    #filename = "BA_matrix_train,L=10,mu=[1,3],delta=1.npz"
    #filename = "BA_matrix_train,L=10,mu=[0,49],delta=1.npz"
    #filename = "BA_matrix_train,L=10,mu=[0,99],delta=1.npz"
    #filename = "BA_matrix_train,L=20,mu=[0,10],delta=1.npz"
    #filename = "BA_matrix_train,L=20,mu=[0,99],delta=1.npz"
    #filename = "G_eigenvalue_train_L=20_mu=[0,10]_delta=1.npz"
    #filename = "20191201,BA_matrix_train,N=5,delta=0.5,mu=[-10, 1, 3, 14].npz"
    f = np.load(path+filename)

    return f["arr_0"].reshape(5000,-1),f["arr_1"]-1
    #return f["BA"].reshape(4000,-1)[2001:4000],(f["phase"]-1)[2001:4000]
    #return f["arr_0"],f["arr_1"]-1
def test():

    path = "D:/program/vscode_workspace/private/data/project_RBM(phy)/"
    filename = "BA_matrix_test,L=10,mu=[0,10],delta=1.npz"
    #filename = "BA_matrix_test,L=20,mu=[0,10],delta=1.npz"
    #filename = "20191201,BA_matrix_test,N=5,delta=0.5.npz"
    f = np.load(path+filename)

    return f["arr_0"].reshape(10001,-1),f["arr_1"]-1
    #return f["BA"].reshape(5600,-1)[2801:],(f["phase"]-1)[2801:]

# Load Data
X, Y = data()
#X = (X - np.min(X, 0)) / (np.max(X, 0) + 0.0001)  # 0-1 scaling
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0)

# Models we will use
#logistic = linear_model.LogisticRegression(solver='newton-cg', tol=1)
logistic = KMeans(2)
rbm1 = BernoulliRBM(random_state=0, verbose=True)
rbm2 = BernoulliRBM(random_state=0, verbose=True)
rbm3 = BernoulliRBM(random_state=0, verbose=True)

rbm_features_classifier = Pipeline(steps=[('rbm1', rbm1), ('rbm2', rbm2), ('rbm3', rbm3), ('logistic', logistic)])
# #############################################################################
# Training

# Hyper-parameters. These were set by cross-validation,
# using a GridSearchCV. Here we are not performing cross-validation to
# save time.

batch = 1024
rbm1.batch_size = batch
rbm1.learning_rate = 0.1
rbm1.n_iter = 20
rbm1.n_components = 250

rbm2.batch_size = batch
rbm2.learning_rate = 0.1
rbm2.n_iter = 40
rbm2.n_components = 500

rbm3.batch_size = batch
rbm3.learning_rate = 0.01
rbm3.n_iter = 80
rbm3.n_components = 1000

logistic.C = 6000

# Training RBM-Logistic Pipeline
rbm_features_classifier.fit(X_train)

# Training the Logistic regression classifier directly on the pixel
raw_pixel_classifier = clone(logistic)
raw_pixel_classifier.C = 100.
raw_pixel_classifier.fit(X_train)
# #############################################################################
# Evaluation
Y_pred = rbm_features_classifier.predict(X_test) #這行就是隱藏層的預測
print("經過 RBM 再 Kmean:")
print(Y_pred)
print(Y_test)
print("Logistic regression using RBM features:\n%s" % (metrics.classification_report(Y_test, Y_pred)))
print("X_test accuracy: "+str(metrics.accuracy_score(Y_test, rbm_features_classifier.predict(X_test))))

print("----------------------------------------")
Y_pred = raw_pixel_classifier.predict(X_test)
print("直接 Kmeans:")
print(Y_pred)
print(Y_test)
print("Logistic regression using raw pixel features:\n%s" % (metrics.classification_report(Y_test, Y_pred)))
print("X_test accuracy: "+str(metrics.accuracy_score(Y_test, raw_pixel_classifier.predict(X_test))))
# #############################################################################
# Plotting

X, Y = test()
tmp = rbm_features_classifier.predict(X)
plt.subplot(221)
plt.title("RBM -> Kmean:")
plt.scatter(range(len(tmp)),tmp)

tmp = raw_pixel_classifier.predict(X)
plt.subplot(222)
plt.title("Kmeans:")
plt.scatter(range(len(tmp)),tmp)

tmp = Y
plt.subplot(223)
plt.title("Answer:")
plt.scatter(range(len(tmp)),tmp)
plt.tight_layout()
plt.show()
