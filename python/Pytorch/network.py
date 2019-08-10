import torch
import torch.nn as nn
from torchsummary import summary

flag = 1
while flag==1 :
    N = input("N = ")
    if N == "5":
        internet = [(1, 16, 4, 1, 2),(16, 32, 4, 1, 2),(32 *  7 *  7, 512, 2)] #5x5
        flag = 0
    elif N == "6":
        internet = [(1, 16, 5, 1, 2),(16, 32, 5, 1, 2),(32 *  9 *  9, 512, 2)] #6x6
        flag = 0
    elif N == "7":
        internet = [(1, 16, 4, 1, 2),(16, 32, 4, 1, 2),(32 * 13 * 13, 512, 2)] #7x7
        flag = 0
    elif N == "8":
        internet = [(1, 16, 5, 1, 2),(16, 32, 5, 1, 2),(32 * 16 * 16, 512, 2)] #8x8
        flag = 0
    else:
        print("input the correct N\n")

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

print(cnn)
summary(cnn,(1,int(N)*int(N),int(N)*int(N)),-1)
