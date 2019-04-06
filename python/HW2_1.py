
# coding: utf-8 

# ### Layers : Fundamental blocks of Neural Network

# In[1]:


import torch
from torch.nn import Linear, ReLU
import torch.nn as nn
import numpy as np
from torch.autograd import Variable


# In[2]:


myLayer = Linear(in_features=10,out_features=5,bias=True)
inp = Variable(torch.randn(1,10))
myLayer = Linear(in_features=10,out_features=5,bias=True) 
myLayer(inp)

# In[3]:


myLayer.weight


# In[4]:


myLayer.bias


# ### Stacking Linear layers

# In[5]:


myLayer1 = Linear(10,5)
myLayer2 = Linear(5,2)
myLayer2(myLayer1(inp))


# ### PyTorch Non-linear Activations

# In[6]:


sample_data = Variable(torch.Tensor([[1,2,-1,-1]])) 
myRelu = ReLU()
myRelu(sample_data)
 

# In[7]:


import torch.nn as nn
import torch.nn.functional as F
sample_data = Variable(torch.Tensor([[1,2,-1,-1]])) 
f = F.relu(sample_data) # Much simpler.
f


# ### Neural Network 

# In[8]:


class MyFirstNetwork(nn.Module):
    def __init__(self,input_size,hidden_size,output_size):
        super(MyFirstNetwork,self).__init__() 
        self.layer1 = nn.Linear(input_size,hidden_size) 
        self.layer2 = nn.Linear(hidden_size,output_size)
    def __forward__(self,input): 
        out = self.layer1(input) 
        out = nn.ReLU(out)
        out = self.layer2(out) 
        return out


# ### Loss

# In[9]:


loss = nn.MSELoss()
input = Variable(torch.randn(3, 5), requires_grad=True) 
target = Variable(torch.randn(3, 5))
output = loss(input, target)
output.backward()


# In[10]:


def cross_entropy(true_label, prediction):
    if true_label == 1:
        return -log(prediction)
    else:
        return -log(1 - prediction)


# In[11]:


loss = nn.CrossEntropyLoss()
input = Variable(torch.randn(3, 5), requires_grad=True) 
target = Variable(torch.LongTensor(3).random_(5)) 
output = loss(input, target)
#print(input)
#print(target)
#print(output)
output.backward()


from glob import glob
from PIL import Image
from torch.utils.data import Dataset
# ### Optimizer
class DogsAndCatsDataset(Dataset):
    def __init__(self,root_dir,size=(224,224)):
        self.files = glob(root_dir)
        self.size = size
        self.arr = np.array([[1,0],[1,0],[1,0],[1,0],[0,1],[0,1],[0,1],[0,1],[0,1],[0,1],[0,1],[1,0],
                             [0,1],[0,1],[0,1],[0,1],[1,0],[1,0],[0,1],[0,1],[1,0],[0,1],[1,0],[1,0],
                             [0,1],[1,0],[1,0],[0,1],[0,1],[1,0]], float)
    def __len__(self):
        return len(self.files)
    def __getitem__(self,idx):
        input = Variable(torch.from_numpy(np.asarray(Image.open(self.files[idx]).resize((1,224*224)), float)))
        target = Variable(torch.from_numpy(self.arr[idx])) 
        return input,target

dataset=DogsAndCatsDataset("D:/program/vscode_workspace/private/data/dogs-vs-cats/sample/*.jpg")
#import matplotlib.pylab as plt
#plt.imshow(dataset[0][0])
#plt.show()

# In[14]:

# for demo
import torch.optim as optim
loss_fn = nn.MSELoss()
model1 = nn.Linear(224*224,56*56)
model2 = nn.Linear(56*56,28*28)
model3 = nn.Linear(28*28,2)
optimizer = optim.SGD(model1.parameters(), lr = 0.00001,momentum=0.9)
for input, target in dataset:

    #print(input.float().type())
    #print (model.weight.type())
    data=input[:,:,0].view(1,-1).float()+input[:,:,1].view(1,-1).float()+input[:,:,2].view(1,-1).float()
    output = model1(data/(3*(255.)**2)**0.5)
    output = myRelu(output)
    output = model2(output)
    output = myRelu(output)
    output = model3(output)    
    output = F.softmax(output,dim=1)
    print(output)
    optimizer.zero_grad()
    loss = loss_fn(output, target.float())
    loss.backward()
    optimizer.step()


#a=DogsAndCatsDataset("D:/program/vscode_workspace/private/data/dogs-vs-cats/sample_test/*.jpg")
#print("------------------------")
#data=input[:,:,0].view(1,-1).float()+input[:,:,1].view(1,-1).float()+input[:,:,2].view(1,-1).float()
#output = model3(model2(model1(data/(3*(255.)**2)**0.5)))
#print(output)



def f(x,index):
    sum=0
    for i in range(len(x)):
        sum+=np.e**(x[i])
    return -x[index]+np.log(sum)

a=f([0.0649,0.0901,-0.3965],0)
b=f([-0.2551,0.0602,-0.4174],1)
print((a**2+b**2)**0.5)
print(a,b)
print((a+b)/2)