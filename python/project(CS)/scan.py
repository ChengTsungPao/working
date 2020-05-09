from glob import glob
import numpy as np
import pickle
import warnings
warnings.filterwarnings("ignore")

def health_or_not(X_test_label, X_test_radius, mode):
    ans = 0
    with open("picture.pickle", 'rb') as f:
        model_label = pickle.load(f)
    with open("radius.pickle", 'rb') as f:
        model_radius = pickle.load(f)
    X_test_label = np.array(list(X_test_label.values()))
    X_test_radius = np.array(list(X_test_radius.values()))
    label = model_label.predict(X_test_label)
    radius = model_radius.predict(X_test_radius)
    label_prob = model_label.predict_proba(X_test_label)[:,1]
    radius_prob = model_radius.predict_proba(X_test_radius)[:,1]
    for i in range(len(X_test_label)):
        if(mode == "health"):
            if(label[i] != radius[i]):
                ans += -1
            else:
                ans += label[i] -1 * (label == 0) 
        elif(mode == "unhealth"):
            if(label[i] != radius[i]):
                ans += 1
            else:
                ans += label[i] - 1 * (label == 0)  
        elif(mode == "delete"):
            if(label[i] == radius[i]):
                ans += label[i] - 1 * (label[i] == 0)
        else:
            if(label[i]==0 and radius[i]==1):
                if(1 - label_prob[i] > radius_prob[i]):
                    ans += -1
                else:
                    ans += 1
            elif(label[i]==1 and radius[i]==0):
                if(label_prob[i] > 1 - radius_prob[i]):
                    ans += 1
                else:
                    ans += -1
            else:
                ans += label[i] - 1 * (label[i] == 0)  
    return ans < 0

def radius_update(Radius_data, train_radius_data, train_picture_data, name, unit, filter_mode, ui):
    path = "./{}/".format(name.split(".")[0] + "_" + filter_mode)
    if health_or_not(train_picture_data, train_radius_data, "confidence"):
        ui.result_text.setText("health")
    else:
        ui.result_text.setText("unhealth") 
    while ui.scanner:
        file = glob(path + "*.png")
        if(len(file) != len(Radius_data)):
            del Radius_data[list( set(Radius_data.keys()) - set(file) )[0]]
            del train_picture_data[list( set(train_picture_data.keys()) - set(file) )[0]]
            del train_radius_data[list( set(train_radius_data.keys()) - set(file) )[0]]
            data = np.array(list(Radius_data.values()))      
            ui.inside_text.setText(("%.3f " % round(np.average(data[:,0]), 3)) + str(unit))
            ui.outside_text.setText(("%.3f " % round(np.average(data[:,1]), 3)) + str(unit))  
            if health_or_not(train_picture_data, train_radius_data, "confidence"):
                ui.result_text.setText("health")  
            else:
                ui.result_text.setText("unhealth") 
            

