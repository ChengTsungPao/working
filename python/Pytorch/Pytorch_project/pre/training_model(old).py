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
        x = x.view(x.size(0), -1)   
        x = self.layer(x)
        x = nn.functional.relu(x)
        x = self.out(x)
        output = nn.functional.softmax(x,dim=1)
        return output

class CNN_2D(nn.Module):
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

class CNN_4D(nn.Module):
    def __init__(self,conv1,conv2,linear):
        super(CNN_4D, self).__init__()
        self.conv1 = nn.Sequential(  
            nn.Conv3d(
                in_channels=conv1[0],      
                out_channels=conv1[1],    
                kernel_size=conv1[2],     
                stride=conv1[3],          
                padding=conv1[4],      
            ),      
            nn.ReLU(),    
            nn.MaxPool3d(kernel_size=(2,2,2),stride=(2,2,2)), 
        )
        self.conv2 = nn.Sequential(  
            nn.Conv3d(conv2[0], conv2[1], conv2[2], conv2[3], conv2[4]),  
            nn.ReLU(),  
            nn.MaxPool3d(kernel_size=(2,2,2),stride=(2,2,2)),  
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

def which_line(classify_phase,mode):   
    if mode==False: 
        if(abs(classify_phase[0]-classify_phase[1])==1):
            if(classify_phase[0]==1):
                line = "mu=1"
            elif(classify_phase[0]==3):
                line = "mu=3"
            elif(classify_phase[0]==7):
                line = "mu=5"
            elif(classify_phase[0]==5):
                line = "mu=-1"
        elif(classify_phase[0]%2==1):
            line = "delta=1"
        elif(classify_phase[0]%2==0):
            line = "delta=-1"
        else:
            print("please input the correct phase !!!")
    elif mode==True:
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
    return line

########################################################################################################################################
########################################################################################################################################
########################################################################################################################################

def training1D(network,filename,mode):
    
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

    line = "delta=1"
    classify_phase_test = [5,1,3,7]

    def phmode(ph):
        m = 0
        try:
            if(ph[0]==9 and ph[1]==10 and ph[2]==9):
                m = 1
            elif(ph[0]==9 and ph[1]==10 and ph[2]==11):
                m = 2
            else:
                print("error1") 
        except:
            print("error2") 
        return m    


    def get_train_data(phase):


        file = np.load((path+'/train/{},{}_train,N={},{}.npz').format(particle_data[0],particle_data[1],particle_data[2],line))

        test_input = []
        test_target = []
        train_input = []
        train_target = []

        if(phmode(phase)==1):            
            test_input =   file[kind_of_data[0]][ 800 : 1000].tolist() + \
                           file[kind_of_data[0]][1800 : 2000].tolist() + \
                           file[kind_of_data[0]][2800 : 3000].tolist() + \
                           file[kind_of_data[0]][3800 : 4000].tolist()
            test_target =  file[kind_of_data[1]][ 800 : 1000].tolist() + \
                           file[kind_of_data[1]][1800 : 2000].tolist() + \
                           file[kind_of_data[1]][2800 : 3000].tolist() + \
                           file[kind_of_data[1]][3800 : 4000].tolist()
            train_input =  file[kind_of_data[0]][   0 :  800].tolist() + \
                           file[kind_of_data[0]][1000 : 1800].tolist() + \
                           file[kind_of_data[0]][2000 : 2800].tolist() + \
                           file[kind_of_data[0]][3000 : 3800].tolist()
            train_target = file[kind_of_data[1]][   0 :  800].tolist() + \
                           file[kind_of_data[1]][1000 : 1800].tolist() + \
                           file[kind_of_data[1]][2000 : 2800].tolist() + \
                           file[kind_of_data[1]][3000 : 3800].tolist()
        elif(phmode(phase)==2):
            test_input =   file[kind_of_data[0]][ 800 : 1000].tolist() + \
                           file[kind_of_data[0]][1400 : 1500].tolist() + \
                           file[kind_of_data[0]][2400 : 2500].tolist() + \
                           file[kind_of_data[0]][3800 : 4000].tolist()
            test_target =  file[kind_of_data[1]][ 800 : 1000].tolist() + \
                           file[kind_of_data[1]][1400 : 1500].tolist() + \
                           file[kind_of_data[1]][2400 : 2500].tolist() + \
                           file[kind_of_data[1]][3800 : 4000].tolist()
            train_input =  file[kind_of_data[0]][   0 :  800].tolist() + \
                           file[kind_of_data[0]][1000 : 1400].tolist() + \
                           file[kind_of_data[0]][2000 : 2400].tolist() + \
                           file[kind_of_data[0]][3000 : 3800].tolist()
            train_target = file[kind_of_data[1]][   0 :  800].tolist() + \
                           file[kind_of_data[1]][1000 : 1400].tolist() + \
                           file[kind_of_data[1]][2000 : 2400].tolist() + \
                           file[kind_of_data[1]][3000 : 3800].tolist()
        else:
            print("error")

        test_input = np.array(test_input)
        test_target = np.array(test_target)
        train_input = np.array(train_input)
        train_target = np.array(train_target)

        if(phmode(phase)==1):
            test_target = np.where(test_target==5,9,test_target)
            test_target = np.where(test_target==1,10,test_target)
            test_target = np.where(test_target==3,10,test_target)
            test_target = np.where(test_target==7,9,test_target)
            train_target = np.where(train_target==5,9,train_target)
            train_target = np.where(train_target==1,10,train_target)
            train_target = np.where(train_target==3,10,train_target)
            train_target = np.where(train_target==7,9,train_target)
        elif(phmode(phase)==2):
            test_target = np.where(test_target==5,9,test_target)
            test_target = np.where(test_target==1,10,test_target)
            test_target = np.where(test_target==3,10,test_target)
            test_target = np.where(test_target==7,11,test_target)
            train_target = np.where(train_target==5,9,train_target)
            train_target = np.where(train_target==1,10,train_target)
            train_target = np.where(train_target==3,10,train_target)
            train_target = np.where(train_target==7,11,train_target)

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
        ph = np.array(ph)
        if(phmode(classify_phase)==1):
            ph = np.where(ph==5,9,ph)
            ph = np.where(ph==1,10,ph)
            ph = np.where(ph==3,10,ph)
            ph = np.where(ph==7,9,ph)
        elif(phmode(classify_phase)==2):
            ph = np.where(ph==5,9,ph)
            ph = np.where(ph==1,10,ph)
            ph = np.where(ph==3,10,ph)
            ph = np.where(ph==7,11,ph)
        return TensorDataset(torch.tensor(np.array(data)),torch.tensor(ph))

    test_data_all = get_test_data(classify_phase_test)

    dnn = DNN(internet)  
    dnn = dnn.cuda()     

    def Accuracy(data):        
        s = 0
        for step, (b_x, b_y) in enumerate(data):            
            a = torch.reshape(b_x,(-1,number_of_particle*2))   
            a = a.cuda()
            output = dnn(a.float())   
            index = np.argmax(output[0].cpu().data.numpy())      
            if(int(b_y.numpy())==int(classify_phase[index])):
                s += 1
        return s/len(data)
 
    acc = []  
    train_dataloader = DataLoader(dataset=train_data, batch_size=BATCH_SIZE, shuffle=True, num_workers=2) 
    optimizer = torch.optim.Adam(dnn.parameters(), lr=LR)  
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=STEPLR[0], gamma=STEPLR[1])
    loss_func = nn.CrossEntropyLoss()   
    loss_func = loss_func.cuda() 
    for epoch in range(EPOCH):
        print("epoch:"+str(epoch)+"\n")
        scheduler.step()
        
        for step, (b_x, b_y) in enumerate(train_dataloader):   
            a = torch.reshape(b_x,(-1,number_of_particle*2))
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
            output = dnn(a.float())   
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
    torch.save(dnn, time.strftime("%Y%m%d%H%M", time.localtime())+",phase="+str(classify_phase)+",N="+particle_data[2]+',gpu.pkl')

########################################################################################################################################
########################################################################################################################################
########################################################################################################################################

def training2D(network,filename,mode):
    
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

    line = which_line(classify_phase,mode)

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

    cnn = CNN_2D(internet[0],internet[1],internet[2])  
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

########################################################################################################################################
########################################################################################################################################
########################################################################################################################################

def training4D(network,filename,mode):
    
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
    line = which_line(classify_phase,mode)

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

    cnn = CNN_4D(internet[0],internet[1],internet[2])  
    cnn = cnn.cuda() 

    def Accuracy(data):        
        s = 0
        for step, (b_x, b_y) in enumerate(data):            
            a = torch.reshape(b_x,(-1,int(particle_data[2]),int(particle_data[2]),int(particle_data[2]),int(particle_data[2]))) 
            a = a.cuda()
            output = cnn(a.float())   
            index = np.argmax(output[0].cpu().data.numpy())      
            if(int(b_y.numpy())==int(classify_phase[index])):
                s += 1
        return s/len(data)

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
            a = torch.reshape(b_x,(-1,int(particle_data[2]),int(particle_data[2]),int(particle_data[2]),int(particle_data[2])))
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
