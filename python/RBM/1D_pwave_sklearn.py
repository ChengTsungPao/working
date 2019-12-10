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
    #filename = "G_eigenvalue_train_L=20_mu=[0,10]_delta=1.npz"
    f = np.load(path+filename)

    return f["arr_0"].reshape(5000,-1),f["arr_1"]-1
    #return f["arr_0"],f["arr_1"]-1

# Load Data
X, Y = data()
X = (X - np.min(X, 0)) / (np.max(X, 0) + 0.0001)  # 0-1 scaling
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=0)

# Models we will use
#logistic = linear_model.LogisticRegression(solver='newton-cg', tol=1)
logistic = KMeans(2)
rbm = BernoulliRBM(random_state=0, verbose=True)

rbm_features_classifier = Pipeline(steps=[('rbm', rbm), ('logistic', logistic)])
# #############################################################################
# Training

# Hyper-parameters. These were set by cross-validation,
# using a GridSearchCV. Here we are not performing cross-validation to
# save time.
rbm.learning_rate = 0.06
rbm.n_iter = 10
# More components tend to give better prediction performance, but larger
# fitting time
rbm.n_components = 100
logistic.C = 6000

# Training RBM-Logistic Pipeline
rbm_features_classifier.fit(X_train)

# Training the Logistic regression classifier directly on the pixel
raw_pixel_classifier = clone(logistic)
raw_pixel_classifier.C = 100.
raw_pixel_classifier.fit(X_train, Y_train)
# #############################################################################
# Evaluation
Y_pred = rbm_features_classifier.predict(X_test) #這行就是隱藏層的預測
print("經過 RBM 再 Kmean:")
print(Y_pred)
print(Y_test)
print("Logistic regression using RBM features:\n%s\n" % (metrics.classification_report(Y_test, Y_pred)))
print(metrics.accuracy_score(Y_test, rbm_features_classifier.predict(X_test)))

print("----------------------------------------")
Y_pred = raw_pixel_classifier.predict(X_test)
print("直接 Kmeans:")
print(Y_pred)
print(Y_test)
print("Logistic regression using raw pixel features:\n%s\n" % (metrics.classification_report(Y_test, Y_pred)))
print(metrics.accuracy_score(Y_test, raw_pixel_classifier.predict(X_test)))
# #############################################################################
# Plotting
'''
plt.figure(figsize=(4.2, 4))
for i, comp in enumerate(rbm.components_):
    plt.subplot(10, 10, i + 1)
    plt.imshow(comp.reshape((10, 10)),
               interpolation='nearest')
    plt.xticks(())
    plt.yticks(())
plt.suptitle('100 components extracted by RBM', fontsize=16)
plt.subplots_adjust(0.08, 0.02, 0.92, 0.85, 0.08, 0.23)

plt.show()
'''
