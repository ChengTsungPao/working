import time
import numpy as np
from glob import glob

import torch
import torch.nn as nn
import torch.utils.data as Data
from torch.utils.data import DataLoader, TensorDataset, Dataset


class DNN(nn.Module):
    def __init__(self,linear):
        super(DNN, self).__init__()
        self.layer = nn.Linear(linear[0], linear[1])  
        self.out = nn.Linear(linear[1], linear[2])
    def forward(self, x):
        x = self.layer(x)
        x = self.out(x)
        output = nn.functional.softmax(x,dim=1)
        return output

class CNN(nn.Module):
    def __init__(self,conv1,conv2,linear):
        super(CNN_2D, self).__init__()
        self.conv1 = nn.Sequential(  
            nn.Conv2d(
                in_channels=conv1[0],      
                out_channels=conv1[1],    
                kernel_size=conv1[2],     
                stride=conv1[3],          
                padding=conv1[4],      
            ),      
            nn.ReLU(),    
            nn.MaxPool2d(kernel_size=2), 
        )
        self.conv2 = nn.Sequential(  
            nn.Conv2d(conv2[0], conv2[1], conv2[2], conv2[3], conv2[4]),  
            nn.ReLU(),  
            nn.MaxPool2d(2),  
        )
    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = x.view(x.size(0), -1)   
        return output

def which_line(classify_phase):   
    if(abs(classify_phase[0]-classify_phase[1])==1):
        if(classify_phase[0]==1):
            line = "delta=[0.5, -0.5]" #"mu=1"
        elif(classify_phase[0]==3):
            line = "mu=3"
        elif(classify_phase[0]==7):
            line = "mu=5"
        elif(classify_phase[0]==5):
            line = "mu=-1"
    elif(classify_phase[0]%2==1):
        line = "delta=0.5"
    elif(classify_phase[0]%2==0):
        line = "delta=-0.5"
    else:
        print("please input the correct phase !!!")
    return line

########################################################################################################################################
########################################################################################################################################
########################################################################################################################################

def training(network,filename,dimension):

    path = filename[0]
    classify_phase = filename[1]
    kind_of_data = filename[2]
    particle_data = filename[3]
    number_of_particle = int(particle_data[2])*int(particle_data[2])

    EPOCH = network[0]    
    LR = network[1] 
    STEPLR = network[2]  
    BATCH_SIZE = network[3] 
    internet = network[4] 
  
    line = which_line(classify_phase)

    def move(ph):
        if(line=="delta=0.5" or line=="delta=-0.5"):
            if(ph==5 or ph==6):
                m = 0
            elif(ph==1 or ph==2):
                m = 1000
            elif(ph==3 or ph==4):
                m = 2000
            elif(ph==7 or ph==8):
                m = 3000
            else:
                print("error")
        else:
            if(ph==5 or ph==1 or ph==3 or ph==7):
                m = 0
            elif(ph==6 or ph==2 or ph==4 or ph==8):
                m = 1000
            else:
                print("error")            
        return m

    def get_train_data(phase):

        file = np.load((path+'/train/{},{}_train,N={},{}.npz').format(particle_data[0],particle_data[1],particle_data[2],line))

        test_input = []
        test_target = []
        train_input = []
        train_target = []
        
        for i in range(len(phase)):
            test_input += file[kind_of_data[0]][800 + move(phase[i]) : 1000 + move(phase[i])].tolist()
            test_target += file[kind_of_data[1]][800 + move(phase[i]) : 1000 + move(phase[i])].tolist()
            train_input += file[kind_of_data[0]][0 + move(phase[i]) : 800 + move(phase[i])].tolist()
            train_target += file[kind_of_data[1]][0 + move(phase[i]) : 800 + move(phase[i])].tolist()

        test_input = np.array(test_input)
        test_target = np.array(test_target)
        train_input = np.array(train_input)
        train_target = np.array(train_target)

        return [torch.tensor(test_input  ,dtype=torch.float64),
                torch.tensor(test_target ,dtype=torch.float64),
                torch.tensor(train_input ,dtype=torch.float64),
                torch.tensor(train_target,dtype=torch.float64)]

    def get_test_data(phase):  
        data = []
        ph = []  
        file = np.load((path+'/test/{},{}_test,N={},{}.npz').format(particle_data[0],particle_data[1],particle_data[2],line))
        for i in range(len(phase)):
            cut = [len(file[kind_of_data[1]]),0]     
            for j in range(len(file[kind_of_data[1]])):        
                if(cut[0] > j and int(file[kind_of_data[1]][j])==phase[i]):
                    cut[0] = j
                if(cut[1] < j and int(file[kind_of_data[1]][j])==phase[i]):
                    cut[1] = j 
            data += file[kind_of_data[0]][cut[0]:cut[1]+1].tolist()
            ph += file[kind_of_data[1]][cut[0]:cut[1]+1].tolist()

        return TensorDataset(torch.tensor(np.array(data)),torch.tensor(np.array(ph)))   

    total_data = get_train_data(classify_phase)    
    test_data  = TensorDataset(total_data[0],total_data[1])
    train_data = TensorDataset(total_data[2],total_data[3])
    test_data_all = get_test_data(classify_phase)

    dnn = DNN(internet[2])
    cnn = CNN(internet[0],internet[1])

    dnn = dnn.cuda()
    cnn = cnn.cuda() 

    def Accuracy(data):        
        s = 0
        for step, (b_x, b_y) in enumerate(data):            
            a = torch.reshape(b_x,(-1,2,number_of_particle*2,number_of_particle*2))
            a = a.cuda()
            output = dnn(cnn(a.float()))   
            index = np.argmax(output[0].cpu().data.numpy())      
            if(int(b_y.numpy())==int(classify_phase[index])):
                s += 1
        return s/len(data)
 
    acc = []  
    train_dataloader = DataLoader(dataset=train_data, batch_size=BATCH_SIZE, shuffle=True, num_workers=2) 
    optimizer = torch.optim.Adam(list(cnn.parameters()) + list(dnn.parameters()), lr=LR)  
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=STEPLR[0], gamma=STEPLR[1])
    loss_func = nn.CrossEntropyLoss()   
    loss_func = loss_func.cuda() 
    for epoch in range(EPOCH):
        print("epoch:"+str(epoch)+"\n")
        scheduler.step()
        
        for step, (b_x, b_y) in enumerate(train_dataloader):
            a = torch.reshape(b_x,(-1,2,number_of_particle*2,number_of_particle*2))
            b = []
            for i in b_y.numpy():
                if(int(i)==int(classify_phase[0])):
                    b.append(0)
                elif(int(i)==int(classify_phase[1])):
                    b.append(1)
                elif(int(i)==int(classify_phase[2])):
                    b.append(2)
                elif(int(i)==int(classify_phase[3])):
                    b.append(3)            
            b = torch.tensor(b)            
            a = a.cuda()
            b = b.cuda()
            output = dnn(cnn(a.float()))
            optimizer.zero_grad()      
            loss = loss_func(output, b.long())             
            loss.backward()               
            optimizer.step()             
            if(step%200==0):          
                print("number of data:"+str(step))
                print("output:\n"+str(output.data))
                print("target:\n"+str(b.data))
                print("\n")

        if(epoch%100==0):        
            print("epoch:"+str(epoch))
            print("  training:"+str(Accuracy(train_data)))
            print("  predict :"+str(Accuracy(test_data)))   
            tmp = Accuracy(test_data_all)        
            print("  total_predict :"+str(tmp))
            acc.append(tmp)
    print("\n")
    print(acc)
    torch.save(cnn,time.strftime("%Y%m%d%H%M%S", time.localtime())+",phase={},N={},dim={},{},gpu.pkl".format(str(classify_phase),particle_data[2],str(dimension),"cnn"))
    torch.save(dnn,time.strftime("%Y%m%d%H%M%S", time.localtime())+",phase={},N={},dim={},{},gpu.pkl".format(str(classify_phase),particle_data[2],str(dimension),"dnn"))
