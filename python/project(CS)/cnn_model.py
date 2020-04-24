import torch
import torch.nn as nn
from torchsummary import summary

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
            nn.MaxPool2d(kernel_size=2), 
        )
        self.conv2 = nn.Sequential(  
            nn.Conv2d(32, 64, 5, 1, 2),  
            nn.ReLU(),  
            nn.MaxPool2d(2),
            nn.Dropout(0.25),  
        )
        self.layer = nn.Sequential( 
            nn.Linear(1032256, 512),
            nn.Dropout(0.5),
        )
        self.out = nn.Linear(512, 2)
    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = x.view(x.size(0), -1)   
        x = self.layer(x)
        x = self.out(x)
        output = nn.functional.softmax(x,dim=1)
        return output

cnn = CNN()
#cnn = cnn.cuda()  

print(cnn)
summary(cnn, (3, 511, 511), device='cpu')