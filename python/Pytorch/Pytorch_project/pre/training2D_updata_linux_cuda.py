import numpy as np
from glob import glob

import torch
import torch.nn as nn
import torch.utils.data as Data
from torch.utils.data import DataLoader, TensorDataset, Dataset

#path1 = 'D:/program/vscode_workspace/private/data/project_data/train/{},BA_matrix_train,N={},delta=1.npz'
#path2 = 'D:/program/vscode_workspace/private/data/project_data/test/{},BA_matrix_test,N={},delta=1.npz'
path1 = './data/train/{},BA_matrix_train,N={},delta=1.npz'
path2 = './data/test/{},BA_matrix_test,N={},delta=1.npz'
def get_data(time, N, phase=[5,1]):

    def move(ph):
        if(ph==5):
            m = 0
        elif(ph==1):
            m = 1000
        elif(ph==3):
            m = 2000
        elif(ph==7):
            m = 3000
        else:
            print("error")
        return m

    file = np.load(path1.format(time,N))

    test_input = np.concatenate((file["BA"][800 + move(phase[0]) : 1000 + move(phase[0])],
                                 file["BA"][800 + move(phase[1]): 1000 + move(phase[1])]))
    test_target = np.concatenate((file["phase"][800 + move(phase[0]) : 1000 + move(phase[0])],
                                  file["phase"][800 + move(phase[1]) : 1000 + move(phase[1])]))
    train_input = np.concatenate((file["BA"][0 + move(phase[0]) : 800 + move(phase[0])],
                                  file["BA"][0 + move(phase[1]) : 800 + move(phase[1])]))
    train_target = np.concatenate((file["phase"][0 + move(phase[0]) : 800 + move(phase[0])],
                                   file["phase"][0 + move(phase[1]) : 800 + move(phase[1])]))
    return [torch.tensor(test_input   ,dtype=torch.float64),
            torch.tensor(test_target,dtype=torch.float64),
            torch.tensor(train_input   ,dtype=torch.float64),
            torch.tensor(train_target,dtype=torch.float64)]

def get_test_data(data,phase=[5,1]):    
    cut1 = [len(data["phase"]),0]
    cut2 = [len(data["phase"]),0]       
    for i in range(len(data["phase"])):        
        if(cut1[0] > i and int(data["phase"][i])==phase[0]):
            cut1[0] = i
        if(cut1[1] < i and int(data["phase"][i])==phase[0]):
            cut1[1] = i
        if(cut2[0] > i and int(data["phase"][i])==phase[1]):
            cut2[0] = i
        if(cut2[1] < i and int(data["phase"][i])==phase[1]):
            cut2[1] = i
    
    return cut1,cut2


total_data = get_data("20190804", "6",[5,1])
test_data  = TensorDataset(total_data[0],total_data[1])
train_data = TensorDataset(total_data[2],total_data[3])


def main():      
    train_dataloader = DataLoader(dataset=train_data, batch_size=1, shuffle=True, num_workers=2)   

    for imgs , labels in train_dataloader:
        for i in range(len(imgs)):
            #print(imgs[i])
            #print(labels[i])
            pass
        break

    class CNN(nn.Module):
        def __init__(self,conv1,conv2,linear):
            super(CNN, self).__init__()
            self.conv1 = nn.Sequential(  # input shape (1, 28, 28)
                nn.Conv2d(
                    in_channels=conv1[0],      # input height
                    out_channels=conv1[1],    # n_filters
                    kernel_size=conv1[2],      # filter size
                    stride=conv1[3],           # filter movement/step
                    padding=conv1[4],      #padding=(kernel_size-1)/2 tride=1
                ),      # output shape (16, 28, 28)
                nn.ReLU(),    # activation
                nn.MaxPool2d(kernel_size=2),    #output shape (16, 14, 14)
            )
            self.conv2 = nn.Sequential(  # input shape (16, 14, 14)
                nn.Conv2d(conv2[0], conv2[1], conv2[2], conv2[3], conv2[4]),  # output shape (32, 14, 14)
                nn.ReLU(),  # activation
                nn.MaxPool2d(2),  # output shape (32, 7, 7)
            )
            self.layer = nn.Sequential(
                nn.Linear(linear[0], linear[1]),   # fully connected layer, output 10 classes
                nn.ReLU()
            )
            self.out = nn.Sequential(
                nn.Linear(linear[1], linear[2]),   # fully connected layer, output 10 classes
                nn.Softmax(dim = 1)
            )        
        def forward(self, x):
            x = self.conv1(x)
            x = self.conv2(x)
            x = x.view(x.size(0), -1)   #(batch_size, 32 * 7 * 7)
            x = self.layer(x)
            output = self.out(x)
            return output

    cnn = CNN((1, 16, 5, 1, 2),(16, 32, 5, 1, 2),(32 * 9 * 9, 512, 2))
    cnn = cnn.cuda()

    def Accuracy(data):        
        s = 0
        for step, (b_x, b_y) in enumerate(data):
            a = torch.reshape(b_x,(1,36,36))
            a = torch.reshape(a,(1,1,36,36))   
            a = a.cuda()
            output = cnn(a.float())         
            if(b_y.numpy()<3 and output[0][0]>output[0][1]):
                s += 1 
            elif(b_y.numpy()>3 and output[0][0]<output[0][1]):
                b = torch.tensor([1])
                s += 1
        return s/len(data)
             


    EPOCH = 1000
    LR = 0.00001      
    optimizer = torch.optim.Adam(cnn.parameters(), lr=LR)   # optimize all cnn parameters
    loss_func = nn.CrossEntropyLoss()   # the target label is not one-hotted  
    loss_func = loss_func.cuda()
    acc = []  
    for epoch in range(EPOCH):
        

        
        for step, (b_x, b_y) in enumerate(train_dataloader):   #batch data, normalize x when iterate train_loader
            #print(b_y)
            a = torch.reshape(b_x,(1,36,36))
            a = torch.reshape(a,(1,1,36,36))            
            if(b_y.numpy()<3):
                b = torch.tensor([0])
            else:
                b = torch.tensor([1])
            a = a.cuda()
            b = b.cuda()
            output = cnn(a.float())               # cnn output
            #print(output[0])
            loss = loss_func(output, b.long())   # cross entropy loss
            optimizer.zero_grad()           # clear gradients for this training step
            loss.backward()                 # backpropagation, compute gradients
            optimizer.step()               # apply gradients  
            #if(step%100==0):          
            #    print("  number of data:"+str(step))
            #    print("    output:"+str(output[0]))
            #    print("    target:"+str(b))
            
        if(epoch%10==0):        
            print("epoch:"+str(epoch))
            print("  training:"+str(Accuracy(train_data)))
            print("  predict :"+str(Accuracy(test_data)))
            file = np.load(path2.format("20190804","6"))
            r = get_test_data(file,[5,1])
            #print(r)
            test1 = TensorDataset(torch.tensor(file["BA"][r[0][0]:r[0][1]]),torch.tensor(file["phase"][r[0][0]:r[0][1]]))
            test2 = TensorDataset(torch.tensor(file["BA"][r[1][0]:r[1][1]]),torch.tensor(file["phase"][r[1][0]:r[1][1]]))
            tmp = (Accuracy(test1)*len(test1)+Accuracy(test2)*len(test2))/(len(test1)+len(test2))
            print("  total_predict :"+str(tmp))
            acc.append(tmp)
    print(acc)
    
if __name__ == '__main__':
    main()




    
#for i in range(1):
#    print(dataloader.dataset[i])
#file = np.load("./data/train/20190804,BA_matrix_train,N=5,delta=1.npz")
#print(np.concatenate((file["phase"][0:5],file["phase"][5:10])))
'''
file = np.load("./data/train/20190804,BA_matrix_train,N=5,delta=1.npz")
print(file["BA"][0])
print(file["phase"][0])


print(np.asarray([[1,2],[1,2]]))
'''