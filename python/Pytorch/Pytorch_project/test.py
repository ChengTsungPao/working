import numpy as np
path = 'D:/program/vscode_workspace/private/data/project_data'
particle_data = ["20190811","6"]
file = np.load((path+'/test/{},BA_matrix_test,N={},delta=-1.npz').format(particle_data[0],particle_data[1]))
s = [0,0,0,0]
for i in range(len(file["phase"])):    
    #print(file["phase"][i])
    if(int(file["phase"][i])==6):
        s[0] += 1
    elif(int(file["phase"][i])==2):
        s[1] += 1
    elif(int(file["phase"][i])==3):
        s[2] += 1   
    elif(int(file["phase"][i])==8):
        s[3] += 1

print(s)

def get_test_data(data,phase):    
    cut = [len(data["phase"]),0]     
    for i in range(len(data["phase"])):        
        if(cut[0] > i and int(data["phase"][i])==phase):
            cut[0] = i
        if(cut[1] < i and int(data["phase"][i])==phase):
            cut[1] = i  
    return data["BA"][cut[0]:cut[1]+1],data["phase"][cut[0]:cut[1]+1]

print(len(get_test_data(file,5)[1]))
print(len(get_test_data(file,1)[1]))
print(len(get_test_data(file,3)[1]))
print(len(get_test_data(file,7)[1]))

print(len([1,2,3]))

