from glob import glob
import numpy as np

def radius_update(Radius_data, name, filter_mode, ui):
    path = "./{}/".format(name.split(".")[0] + "_" + filter_mode)
    while ui.scanner:
        file = glob(path + "*.png")
        if(len(file) != len(Radius_data)):
            del Radius_data[list( set(Radius_data.keys()) - set(file) )[0]]
            data = np.array(list(Radius_data.values()))
            ui.inside_text.setText(str(round(np.average(data[:,0]), 3)))
            ui.outside_text.setText(str(round(np.average(data[:,1]), 3)))              
    
            

