import numpy as np
import torch
from torch.utils.data import DataLoader, TensorDataset
from glob import glob
import torch
import torch.nn as nn
import torch.utils.data as Data

# Goal is to complete dataloader

# 1.Load file name and setup a dictionary to store data
file_dir = glob(".\\data\\*\\*.npz")
full_data_set = {}

keylist=[]
for file in file_dir:
    N = file.split('\\')[-1].split(',')[-2][-1]
    if N not in keylist:
        keylist.append(N)
for N in np.sort(keylist):
    full_data_set[N] = {'train':{'BA':[], 'phase':[]},
                        'test' :{'BA':[], 'phase':[]} }
#del(keylist)

# dictionary structure:
# full_data_set[N= '5'\'6'\'7'\'8'][ 'train'\'test' ][ 'BA'\'phase' ]


# 2.Load data, and store in dictionary

for file in file_dir:
    N = file.split('\\')[-1].split(',')[-2][-1]
    t = file.split('\\')[2]
    data = np.load(file)
    full_data_set[N][t]['BA'].append(data['BA'])
    full_data_set[N][t]['phase'].append(data['phase'])

tensor_data = {}
N_batch = 2


for size in list(full_data_set.keys()):
    for work in ['train','test']:
        tensor_data[size + work]=DataLoader(
            dataset = TensorDataset(torch.tensor(full_data_set[size][work]['BA'],dtype = torch.float64),
                                    torch.tensor(full_data_set[size][work]['phase'],dtype = torch.float64)),
            batch_size=N_batch,
            shuffle=True,
            num_workers=1)





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
        self.out = nn.Linear(linear[0], linear[1])   # fully connected layer, output 10 classes

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = x.view(x.size(0), -1)   #(batch_size, 32 * 7 * 7)
        output = self.out(x)
        return output

cnn = CNN((1, 16, 5, 1, 2),(16, 32, 5, 1, 2),(32 * 9 * 9, 2))


EPOCH = 1          
LR = 0.001  
train_loader = tensor_data["6train"]
optimizer = torch.optim.Adam(cnn.parameters(), lr=LR)   # optimize all cnn parameters
loss_func = nn.CrossEntropyLoss()   # the target label is not one-hotted

def main():
    for epoch in range(EPOCH):
        print("epoch:"+str(epoch))
        b_x = train_loader.dataset[0][0]
        b_y = train_loader.dataset[0][1]
        print(b_y)
        
        for step in range(len(train_loader.dataset[0][1])):   #batch data, normalize x when iterate train_loader

            #print(b_y)
            a = torch.reshape(b_x[step],(1,36,36))
            a = torch.reshape(a,(1,1,36,36))
            print(b_y[step])
            if(b_y[step].numpy()<6):
                b = torch.tensor([0])
            else:
                b = torch.tensor([1])
            output = cnn(a.float())               # cnn output
            loss = loss_func(output, b.long())   # cross entropy loss
            optimizer.zero_grad()           # clear gradients for this training step
            loss.backward()                 # backpropagation, compute gradients
            optimizer.step()                # apply gradients
            print("  step:"+str(step))
    

if __name__ == '__main__':
    main()
# training and testing



