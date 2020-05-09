import cv2
import copy
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from sklearn import linear_model, metrics
from sklearn.model_selection import train_test_split
import warnings
import time
from prettytable import PrettyTable

warnings.filterwarnings('ignore')

def get_data(path):
    health_radius = np.load(path+"health_single.npz")["r"]
    unhealth_radius = np.load(path+"unhealth_single.npz")["r"]
    X_radius = np.array(health_radius.tolist() + unhealth_radius.tolist())
    Y = np.array([0. for _ in range(len(health_radius))] + [1. for _ in range(len(unhealth_radius))])

    health_filename = np.load(path+"health_single.npz")["filename"].tolist()
    unhealth_filename = np.load(path+"unhealth_single.npz")["filename"].tolist()
    filename = health_filename + unhealth_filename
    X = []
    for i, file in enumerate(filename):
        X.append(np.array([X_radius[i], np.array(cv2.imread(file),float).flatten()/255.]))
    X = np.array(X)
    return X, Y, X_radius

path = "./erythrocyte/"
X, Y, X_radius = get_data(path)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, shuffle=True)
print("number of data:",len(X))

#########################################################################################

# radius
radius_train = []
radius_test = []
radius_total = []
for train in X_train[:,0]:
    radius_train.append(train.tolist())
for test in X_test[:,0]:
    radius_test.append(test.tolist())
for total in X[:,0]:
    radius_total.append(total.tolist())
radius_train = np.array(radius_train)    
radius_test = np.array(radius_test)  
radius_total = np.array(radius_total) 

t = time.perf_counter()

model = linear_model.LogisticRegression()
model.fit(radius_train, Y_train)

Y_pred = model.predict(radius_test)
print("LogisticRegression:\n%s" % (metrics.classification_report(Y_test, Y_pred)))
print("X_test accuracy: "+str(metrics.accuracy_score(Y_test, Y_pred)))
print("----------------------------------------")

radius_prob = model.predict_proba(radius_total)[:,1]
radius_pred = model.predict(radius_total)

radius_time = time.perf_counter() - t

#########################################################################################

# label
label_train = []
label_test = []
label_total = []
for train in X_train[:,1]:
    label_train.append(train.tolist())
for test in X_test[:,1]:
    label_test.append(test.tolist())
for total in X[:,1]:
    label_total.append(total.tolist())
label_train = np.array(label_train)    
label_test = np.array(label_test)  
label_total = np.array(label_total) 

t = time.perf_counter()

model = linear_model.LogisticRegression()
model.fit(label_train, Y_train)

Y_pred = model.predict(label_test)
print("LogisticRegression:\n%s" % (metrics.classification_report(Y_test, Y_pred)))
print("X_test accuracy: "+str(metrics.accuracy_score(Y_test, Y_pred)))
print("----------------------------------------")

label_prob = model.predict_proba(label_total)[:,1]
label_pred = model.predict(label_total)

label_time = time.perf_counter() - t

#########################################################################################

name = np.load(path+"health_single.npz")["filename"].tolist() + np.load(path+"unhealth_single.npz")["filename"].tolist()
table = PrettyTable(['name','label_prob','label_pred','radius_prob','radius_pred'])
for i in range(len(radius_pred)):
    if(label_pred[i]==0):
        target_label_pred="health"
    else:
        target_label_pred="unhealth"

    if(radius_pred[i]==0):
        target_radius_pred="health"
    else:
        target_radius_pred="unhealth"

    table.add_row([name[i], round(label_prob[i], 6), target_label_pred, round(radius_prob[i], 6), target_radius_pred])
print(table)
print("radius_time:",radius_time)
print("label_time",label_time)

plt.subplot(221)
plt.title("radius probability")
plt.scatter(range(len(X)),radius_prob)
plt.subplot(222)
plt.title("radius predict")
plt.scatter(range(len(X)),radius_pred, color = "r")
plt.subplot(223)
plt.title("label probability")
plt.scatter(range(len(X)),label_prob)
plt.subplot(224)
plt.title("label predict")
plt.scatter(range(len(X)),label_pred, color = "r")
plt.tight_layout()
plt.show()


