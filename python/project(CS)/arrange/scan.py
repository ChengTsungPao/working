from glob import glob
import numpy as np
import warnings
warnings.filterwarnings("ignore")

def radius_update(Radius_data, name, unit, filter_mode, ui):
    path = "./{}/".format(name.split(".")[0] + "_" + filter_mode)
    while ui.scanner:
        file = glob(path + "*.png")
        if(len(file) != len(Radius_data)):
            del Radius_data[list( set(Radius_data.keys()) - set(file) )[0]]
            data = np.array(list(Radius_data.values()))           
            ui.inside_text.setText(("%.3f " % round(np.average(data[:,0]), 3)) + str(unit))
            ui.outside_text.setText(("%.3f " % round(np.average(data[:,1]), 3)) + str(unit))    
            

