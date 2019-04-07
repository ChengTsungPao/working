import torch
from torch.nn import Linear, ReLU
import torch.nn as nn
import numpy as np
from torch.autograd import Variable

myLayer = Linear(in_features=10,out_features=5,bias=True)
inp = Variable(torch.randn(1,10))
myLayer = Linear(in_features=10,out_features=5,bias=True) 
myLayer(inp)

myLayer.weight
myLayer.bias

myLayer1 = Linear(10,5)
myLayer2 = Linear(5,2)
myLayer2(myLayer1(inp))

sample_data = Variable(torch.Tensor([[1,2,-1,-1]])) 
myRelu = ReLU()
myRelu(sample_data)
 
import torch.nn as nn
import torch.nn.functional as F
sample_data = Variable(torch.Tensor([[1,2,-1,-1]])) 
f = F.relu(sample_data) # Much simpler.
f

class MyFirstNetwork(nn.Module):
    def __init__(self,input_size,hidden_size,output_size):
        super(MyFirstNetwork,self).__init__() 
        self.layer1 = nn.Linear(input_size,hidden_size) 
        self.layer2 = nn.Linear(hidden_size,output_size)
    def layer(self):
        first  = [self.layer1.weight.data,self.layer1.bias.data]
        second = [self.layer2.weight.data,self.layer2.bias.data]
        return first,second
    def forward(self,input): 
        out = self.layer1(input) 
        out = F.relu(out)
        out = self.layer2(out) 
        out = F.softmax(out,dim=1)
        return out

model = MyFirstNetwork(56*56*3,28*28*3,2)
model = model.cuda()
print(model)


loss = nn.MSELoss()
input = Variable(torch.randn(3, 5), requires_grad=True) 
target = Variable(torch.randn(3, 5))
output = loss(input, target)
output.backward()

def cross_entropy(true_label, prediction):
    if true_label == 1:
        return -log(prediction)
    else:
        return -log(1 - prediction)

loss = nn.CrossEntropyLoss()
input = Variable(torch.randn(3, 5), requires_grad=True) 
target = Variable(torch.LongTensor(3).random_(5)) 
output = loss(input, target)
output.backward()
print(output.data.item())

def CrossEntropyLoss(input,target):
    sum = 0
    for i in range(len(input)):
        tmp = 0
        for j in range(len(input[0])):
            tmp+=np.e**(input[i][j])
        sum+=-input[i][target[i]]+np.log(tmp)
    return float(sum)/len(input)

print(CrossEntropyLoss(input.data.numpy(),target.data.numpy()))



from glob import glob
from PIL import Image
from torch.utils.data import Dataset
# ### Optimizer
class DogsAndCatsDataset(Dataset):
    def __init__(self,root_dir,size=(56,56)):
        self.files = glob(root_dir)
        self.size = size
        self.arr = np.array([[1,0],[0,1]],float)
    def __len__(self):
        return len(self.files)
    def __getitem__(self,idx):
        input = Variable(torch.from_numpy(np.asarray(Image.open(self.files[idx]).resize((self.size)), float).reshape(1,-1)))
        #tmp=input.data.numpy()[0][0]
        #for i in range(len(input)):    
        #    tmp=np.hstack((input.data.numpy()[i+1][0]))
        
        if(idx<12500):
            target = Variable(torch.from_numpy(self.arr[0]))
        else:
            target = Variable(torch.from_numpy(self.arr[1])) 
        return input,target

dataset=DogsAndCatsDataset("D:/program/vscode_workspace/private/data/dogs-vs-cats/classifier/*.jpg")
#print(len(dataset[0][0][0]))
#print(dataset[0][0])
#print(dataset[0])
#print(dataset[0][0][:,:,0].view(1,-1)+dataset[0][0][:,:,1].view(1,-1))

#tmp=dataset[0][0].data.numpy()[0][0]
#for i in range(50*50):    
#    tmp=np.hstack((tmp,dataset[0][0].data.numpy()[i+1][0]))  
#print(tmp)

import torch.optim as optim
from time import perf_counter
loss_fn = nn.MSELoss()
loss_fn = loss_fn.cuda()
optimizer = optim.SGD(model.parameters(), lr = 0.00001,momentum=0.9)
print("Training......")

index = 0
t1 = perf_counter()
t  = t1

for input, target in dataset:
    if torch.cuda.is_available():
        input = Variable(input.cuda())
        target = Variable(target.cuda())
    else:
        input, target = Variable(input), Variable(target)
    #data=input[:,:,0].view(1,-1).float()+input[:,:,1].view(1,-1).float()+input[:,:,2].view(1,-1).float()
    data=input.float()
    output = model(data)
    optimizer.zero_grad()
    loss = loss_fn(output, target.float())
    loss.backward()
    optimizer.step()
    index+=1
    if(perf_counter()-t > 30):
        t = perf_counter()
        print("Completion ratio :",str(index*100.0/25000)+"%")
        
t2  = perf_counter()

print(model)
print("--------------------------------------")
print("layer1 :","\nweight :\n",model.layer()[0][0].cpu().numpy(),"\nbias :\n",model.layer()[0][1].cpu().numpy())
print("")
print("layer2 :","\nweight :\n",model.layer()[1][0].cpu().numpy(),"\nbias :\n",model.layer()[1][1].cpu().numpy())
print("time :",str((t2-t1)/60.0)+"min")

print("\ntest.....")
test = DogsAndCatsDataset("D:/program/vscode_workspace/private/data/dogs-vs-cats/sample_test/*.jpg")
#data=input[:,:,0].view(1,-1).float()+input[:,:,1].view(1,-1).float()+input[:,:,2].view(1,-1).float()
output1 = test[0][0].cuda()
output2 = test[1][0].cuda()
output1 = model(output1.float())
output2 = model(output2 .float())
print(output1)
print(output2)