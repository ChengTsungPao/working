import time
import numpy as np
from glob import glob

import torch
import torch.nn as nn
import torch.utils.data as Data
from torch.utils.data import DataLoader, TensorDataset, Dataset

#path = 'D:/program/vscode_workspace/private/data/project_data'
path = './data'
classify_phase = [5,1]
kind_of_data = ["BA","phase"]
particle_data = ["20190804","BA_matrix","6"]
number_of_particle = int(particle_data[2])*int(particle_data[2])

EPOCH = 1    
LR = 0.001  
STEPLR = [EPOCH,0] 
BATCH_SIZE = 3
internet = [(1, 16, 5, 1, 2),(16, 32, 5, 1, 2),(32 * 9 * 9, 512, 2)]

if(abs(classify_phase[0]-classify_phase[1])==1):
    if(classify_phase[0]==1):
        line = "mu=1.0"
    elif(classify_phase[0]==3):
        line = "mu=3.0"
    elif(classify_phase[0]==7):
        line = "mu=5.0"
    elif(classify_phase[0]==5):
        line = "mu=-1.0"
elif(classify_phase[0]%2==1):
    line = "delta=1"
elif(classify_phase[0]%2==0):
    line = "delta=-1"
else:
    print("please input the correct phase !!!")

def get_train_data(phase):

    def move(ph):
        if(line=="delta=1" or line=="delta=-1"):
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

    return [torch.tensor(test_input   ,dtype=torch.float64),
            torch.tensor(test_target,dtype=torch.float64),
            torch.tensor(train_input   ,dtype=torch.float64),
            torch.tensor(train_target,dtype=torch.float64)]

total_data = get_train_data(classify_phase)
test_data  = TensorDataset(total_data[0],total_data[1])
train_data = TensorDataset(total_data[2],total_data[3])

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

test_data_all = get_test_data(classify_phase)

class CNN(nn.Module):
    def __init__(self,conv1,conv2,linear):
        super(CNN, self).__init__()
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
        self.layer = nn.Linear(linear[0], linear[1])  
        self.out = nn.Linear(linear[1], linear[2])
    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = x.view(x.size(0), -1)   
        x = self.layer(x)
        x = self.out(x)
        output = nn.functional.softmax(x,dim=1)
        return output

cnn = CNN(internet[0],internet[1],internet[2])  
cnn = cnn.cuda() 

def Accuracy(data):        
    s = 0
    for step, (b_x, b_y) in enumerate(data):            
        a = torch.reshape(b_x,(-1,1,number_of_particle,number_of_particle))   
        a = a.cuda()
        output = cnn(a.float())   
        index = np.argmax(output[0].cpu().data.numpy())      
        if(int(b_y.numpy())==int(classify_phase[index])):
            s += 1
    return s/len(data)

def main():
    acc = []  
    train_dataloader = DataLoader(dataset=train_data, batch_size=BATCH_SIZE, shuffle=True, num_workers=2) 
    optimizer = torch.optim.Adam(cnn.parameters(), lr=LR)  
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=STEPLR[0], gamma=STEPLR[1])
    loss_func = nn.CrossEntropyLoss()   
    loss_func = loss_func.cuda() 
    for epoch in range(EPOCH):
        print("epoch:"+str(epoch)+"\n")
        scheduler.step()
        for step, (b_x, b_y) in enumerate(train_dataloader):   
            a = torch.reshape(b_x,(-1,1,number_of_particle,number_of_particle))
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
            output = cnn(a.float())   
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
    torch.save(cnn, time.strftime("%Y%m%d%H%M", time.localtime())+",phase="+str(classify_phase)+",N="+particle_data[2]+',gpu.pkl')
    
if __name__ == '__main__':
    main()
