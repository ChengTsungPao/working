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
    #filename = "BA_matrix_test,L=10,mu=[0,10],delta=1.npz"
    filename = "BA_matrix_test,L=10,mu=[-10,10],delta=1.npz"
    #filename = "BA_matrix_test,L=20,mu=[0,10],delta=1.npz"
    #filename = "20191201,BA_matrix_test,N=5,delta=0.5.npz"
    f = np.load(path+filename)

    #return f["arr_0"].reshape(10001,-1),f["arr_1"]-1
    return f["arr_0"].reshape(20001,-1),(f["arr_1"])
    #return f["BA"].reshape(5600,-1)[2801:],(f["phase"]-1)[2801:]
    #return f["arr_0"],f["arr_1"]-1

# Load Data
X, Y = data()
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0)

# Models we will use
#logistic = linear_model.LogisticRegression(solver='newton-cg', tol=1)
logistic = KMeans(3)
rbm = BernoulliRBM(random_state=0, verbose=True)

rbm_features_classifier = Pipeline(steps=[('rbm', rbm), ('logistic', logistic)])
# #############################################################################
# Training

# Hyper-parameters. These were set by cross-validation,
# using a GridSearchCV. Here we are not performing cross-validation to
# save time.
rbm.batch_size = 2048
rbm.learning_rate = 0.01
rbm.n_iter = 10
# More components tend to give better prediction performance, but larger
# fitting time
rbm.n_components = 1000
logistic.C = 1

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
dx = 1
axis = np.linspace(-10,10,len(X))[::dx]
tmp = rbm_features_classifier.predict(X)[::dx]
plt.subplot(221)
plt.title("RBM -> Kmean:")
plt.scatter(axis,tmp)

tmp = raw_pixel_classifier.predict(X)[::dx]
plt.subplot(222)
plt.title("Kmeans:")
plt.scatter(axis,tmp)

tmp = Y[::dx]
plt.subplot(223)
plt.title("Answer:")
plt.scatter(axis,tmp)
plt.tight_layout()
plt.show()
