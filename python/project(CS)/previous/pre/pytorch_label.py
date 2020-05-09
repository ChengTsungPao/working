import time
import cv2
import numpy as np
from glob import glob
import matplotlib.pylab as plt

import torch
import torch.nn as nn
import torch.utils.data as Data
from torch.utils.data import DataLoader, TensorDataset, Dataset
from sklearn.model_selection import train_test_split


class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = nn.Sequential(  
            nn.Conv2d(
                in_channels=3,      
                out_channels=32,    
                kernel_size=5,     
                stride=1,          
                padding=2,      
            ),      
            nn.ReLU(),    
            nn.MaxPool2d(kernel_size=4), 
        )
        self.conv2 = nn.Sequential(  
            nn.Conv2d(32, 64, 5, 1, 2),  
            nn.ReLU(),  
            nn.MaxPool2d(4),  
        )
        self.layer = nn.Linear(63488, 512)  
        self.out = nn.Linear(512, 2)
    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = x.view(x.size(0), -1)   
        x = self.layer(x)
        x = self.out(x)
        output = nn.functional.softmax(x,dim=1)
        return output

def get_data(path):
    health = glob(path+"health/*.bmp")
    unhealth = glob(path+"unhealth/*.bmp")
    filename = health + unhealth
    X = []
    #Y = np.array([[0., 1.] for _ in range(len(health))] + [[1., 0.] for _ in range(len(unhealth))])
    Y = np.array([0. for _ in range(len(health))] + [1. for _ in range(len(unhealth))])
    for f in filename:
        X.append(np.array(cv2.imread(f),float)/255.)
    X = np.array(X)
    X.reshape(len(health) + len(unhealth), -1)
    return X, Y

def Accuracy(data):        
    s = 0
    for step, (b_x, b_y) in enumerate(data): 
        #print(np.shape(b_x))           
        output = model(torch.reshape(b_x,(-1, 3, 511, 512)).cuda().float())     
        if(int(b_y.numpy())==int(np.argmax(output[0].cpu().data.numpy()))):
            s += 1
    return s/len(data)

c = 0.1
EPOCH = 100
BATCH_SIZE = 1
LR = 0.000001
STEPLR = [1, 1]
path = "D:/program/vscode_workspace/private/data/project_image(CS)/"
X, Y = get_data(path)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, shuffle=True)

train_data = TensorDataset(torch.tensor(X_train),torch.tensor(Y_train))
test_data = TensorDataset(torch.tensor(X_test),torch.tensor(Y_test))
train_dataloader = DataLoader(dataset=train_data, batch_size=BATCH_SIZE, shuffle=True, num_workers=2) 

model = CNN()
model = model.cuda()

Train = []
Test = []
optimizer = torch.optim.Adam(model.parameters(), lr=LR)  
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=STEPLR[0], gamma=STEPLR[1])
loss_func = nn.CrossEntropyLoss()   
loss_func = loss_func.cuda() 
for epoch in range(EPOCH):
    print("epoch:"+str(epoch)+"\n")
    scheduler.step()
    
    for step, (b_x, b_y) in enumerate(train_dataloader):
        output = model(torch.reshape(b_x,(-1, 3, 511, 512)).cuda().float())   
        optimizer.zero_grad()      
        loss = loss_func(output, torch.tensor(b_y.cuda()).long())             
        loss.backward()               
        optimizer.step()                     
        #print("number of data:"+str(step))
        #print("output:\n"+str(output.data))
        #print("target:\n"+str(b_y.data))
        #print("\n")

    if(epoch%10==0):
        train, test = Accuracy(train_data), Accuracy(test_data)       
        print("epoch:"+str(epoch))
        print("  training:"+str(train))
        print("  predict :"+str(test))
        Train.append(train)
        Test.append(test)   

print(Accuracy(test_data))

plt.plot(range(len(Train)),Train,"o",label = "train")
plt.plot(range(len(Test)),Test,"o",label = "test")
plt.savefig("test.png")
plt.show()