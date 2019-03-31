
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
output.backward()


# ### Optimizer

# In[14]:


# for demo
import torch.optim as optim
model = nn.Linear(1,1)
optimizer = optim.SGD(model.parameters(), lr = 0.01,momentum=0.9)
for input, target in dataset:
    optimizer.zero_grad()
    output = model(input)
    loss = loss_fn(output, target)
    loss.backward()
    optimizer.step()

