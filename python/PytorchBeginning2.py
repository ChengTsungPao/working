
# coding: utf-8

# In[1]:


import torch
torch.__version__


# In[2]:


import numpy as np
import matplotlib.pyplot as plt
#get_ipython().run_line_magic('matplotlib', 'inline')

from torch.autograd import Variable


# ## First Neural Network Using Pytorch
# 
# We present our first neural network which learns to map training examples (input array) to targets (output array). 
# Lets assume that we work for one of the largest online companies called Wondemovies, which is into serving videos on-demand. Our training dataset contains a feature which represents average hours spent by users watching movies in the platform, we would like to predict how much time each user would spend on the platform in the coming week. Its just a imaginary use case, don't think too much about it. Some of the high level activities for building such a solution are:
# 
# 1. Data preperation : **get_data()** function prepares the tensors (arrays) containing input and output data.
# 2. Create learnable parameters : **get_weights()** function provides us with tensors containing random values , which we will optimize to solve our problem.
# 3. Network Model : **simple_network()** produces the output for the input data applying a linear rule , multiply weights with input data and add the bias term (y = Wx+b).
# 4. Loss : **loss_fn()** provides information about how good the model is.
# 5. Optimizer : **optimize()** function helps us in adjusting random weights created initially to help the model calculate target values more accurately.

# In[3]:


# Training Data
def get_data():
    train_X = np.asarray([3.3,4.4,5.5,6.71,6.93,4.168,9.779,6.182,7.59,2.167,
                         7.042,10.791,5.313,7.997,5.654,9.27,3.1])
    train_Y = np.asarray([1.7,2.76,2.09,3.19,1.694,1.573,3.366,2.596,2.53,1.221,
                         2.827,3.465,1.65,2.904,2.42,2.94,1.3])
    dtype = torch.FloatTensor
    X = Variable(torch.from_numpy(train_X).type(dtype),requires_grad=False).view(17,1)
    y = Variable(torch.from_numpy(train_Y).type(dtype),requires_grad=False)
    return X,y # X, y are tensors now!

def plot_variable(x,y,z='',**kwargs):
    l = []
    for a in [x,y]:
        if type(a) == torch.Tensor: # Change Variable to torch.Tensor
            l.append(a.data.numpy())
    plt.plot(l[0],l[1],z,**kwargs)
    
def get_weights():
    w = Variable(torch.randn(1),requires_grad=True)
    b = Variable(torch.randn(1),requires_grad=True)
    return w,b

def simple_network(x):
    y_pred = torch.matmul(x,w)+b
    return y_pred

def loss_fn(y,y_pred):
    loss = (y_pred-y).pow(2).sum()
    for param in [w,b]:
        if not param.grad is None: param.grad.data.zero_()
    loss.backward()
    return loss.data.numpy() # Modified "return loss.data[0]" to .numpy()

def optimize(learning_rate):
    w.data -= learning_rate * w.grad.data
    b.data -= learning_rate * b.grad.data

learning_rate = 1e-4


# In[5]:


x,y = get_data()               # x - represents training data, y - represents target variables
w,b = get_weights()            # w,b - Learnable parameters
for i in range(1000):
    y_pred = simple_network(x) # function which computes wx + b
    loss = loss_fn(y, y_pred)  # calculates sum of the squared differences of y and y_pred
    if i % 50 == 0: 
        print(loss)
    optimize(learning_rate)    # Adjust w,b to minimize the loss


# In[6]:


#x_numpy = x.data.numpy()
plt.subplot(224)
plot_variable(x, y, 'ro')
plot_variable(x, y_pred, label='Fitted line')


# ## Tensor introduction

# ### Scalar

# In[8]:


x = torch.rand(10)
x.size()


# ### Vector

# In[9]:


temp = torch.FloatTensor([23,24,24.5,26,27.2,23.0])
temp.size()


# ### Matrix

# In[14]:


from sklearn.datasets import load_boston
boston = load_boston()
print(boston.data.shape)


# In[15]:


boston.feature_names


# In[16]:


boston_tensor = torch.from_numpy(boston.data)
boston_tensor.size()


# In[17]:


boston_tensor[:2]


# In[18]:


boston_tensor[:10,:5]


# ### 3d- tensor

# In[ ]:


from PIL import Image

panda = np.array(Image.open('panda.jpg').resize((224,224)))
panda_tensor = torch.from_numpy(panda)
panda_tensor.size()


# In[ ]:

plt.subplot(221)
plt.imshow(panda);


# ### Slicing Tensor

# In[19]:


sales = torch.FloatTensor([1000.0,323.2,333.4,444.5,1000.0,323.2,333.4,444.5])


# In[20]:


sales[:5]


# In[21]:


sales[:-5]


# In[ ]:

plt.subplot(222)
plt.imshow(panda_tensor[:,:,0].numpy());


# In[ ]:

plt.subplot(223)
plt.imshow(panda_tensor[25:175,60:130,0].numpy());
plt.show()


# ### Select specific element of tensor

# In[22]:


#torch.eye(shape) produces an diagonal matrix with 1 as it diagonal #elements.
sales = torch.eye(3,3)
sales[0,1]


# ### 4D Tensor

# In[ ]:


from glob import glob
#Read cat images from disk
data_path='/Users/vishnu/Documents/fastAIPytorch/fastai/courses/dl1/data/dogscats/train/cats/'
cats = glob(data_path+'*.jpg')
#Convert images into numpy arrays
cat_imgs = np.array([np.array(Image.open(cat).resize((224,224))) for cat in
cats[:64]])
cat_imgs = cat_imgs.reshape(-1,224,224,3)
cat_tensors = torch.from_numpy(cat_imgs)
cat_tensors.size()


# ### Tensor addition and multiplication

# In[ ]:


#Various ways you can perform tensor addition
a = torch.rand(2,2) 
b = torch.rand(2,2)
c = a + b
d = torch.add(a,b)
#For in-place addition
a.add_(5)

#Multiplication of different tensors

a*b
a.mul(b)
#For in-place multiplication
a.mul_(b)


# ### On GPU

# In[ ]:


a = torch.rand(10000,10000)
b = torch.rand(10000,10000)

a.matmul(b)
#Time taken : 3.23 s


# In[ ]:


#Move the tensors to GPU
a = a.cuda()
b = b.cuda()
a.matmul(b)
#Time taken : 11.2 µs  


# ### Variables

# In[23]:


from torch.autograd import Variable
x = Variable(torch.ones(2,2),requires_grad=True)
y = x.mean()
y.backward()
x.grad


# In[24]:


x.grad_fn


# In[25]:


x.data


# In[26]:


y.grad_fn


# ### Create data for our neural network

# In[ ]:


def get_data():
    train_X = np.asarray([3.3,4.4,5.5,6.71,6.93,4.168,9.779,6.182,7.59,2.167,
                         7.042,10.791,5.313,7.997,5.654,9.27,3.1])
    train_Y = np.asarray([1.7,2.76,2.09,3.19,1.694,1.573,3.366,2.596,2.53,1.221,
                         2.827,3.465,1.65,2.904,2.42,2.94,1.3])
    dtype = torch.FloatTensor
    X = Variable(torch.from_numpy(train_X).type(dtype),requires_grad=False).view(17,1)
    y = Variable(torch.from_numpy(train_Y).type(dtype),requires_grad=False)
    return X,y


# ### Create learnable parameters

# In[ ]:


def get_weights():
    w = Variable(torch.randn(1),requires_grad = True)
    b = Variable(torch.randn(1),requires_grad=True)
    return w,b


# ### Implement Neural Network

# In[ ]:


def simple_network(x):
    y_pred = torch.matmul(x,w)+b
    return y_pred


# ### Implement Neural Network in Pytorch

# In[ ]:


import torch.nn as nn
f = nn.Linear(17,1) # Much simpler.
f


# ### Implementing Loss Function

# In[ ]:


def loss_fn(y,y_pred):
    loss = (y_pred-y).pow(2).sum()
    for param in [w,b]:
        if not param.grad is None: param.grad.data.zero_()
    loss.backward()
    return loss.data[0]


# In[ ]:


### Implementing Optimizer


# In[ ]:


def optimize(learning_rate):
    w.data -= learning_rate * w.grad.data
    b.data -= learning_rate * b.grad.data


# ## Loading Data

# ### Defining Dataset

# In[ ]:


from torch.utils.data import Dataset
class DogsAndCatsDataset(Dataset):
    def __init__(self,):
        pass
    def __len__(self):
        pass
    def __getitem__(self,idx):
        pass


# In[ ]:


class DogsAndCatsDataset(Dataset):
    def __init__(self,root_dir,size=(224,224)):
        self.files = glob(root_dir)
        self.size = size
    def __len__(self):
        return len(self.files)
    def __getitem__(self,idx):
        img = np.asarray(Image.open(self.files[idx]).resize(self.size))
        label = self.files[idx].split('/')[-2]
        return img,label


# ### Defining DataLoader to iterate over Dogs and Cats Dataset

# In[ ]:

'''
from torch.utils.data import Dataset, DataLoader

dataloader = DataLoader(DogsAndCatsDataset,batch_size=32,num_workers=2)
for imgs , labels in dataloader:
        #Apply your DL on the dataset.
    pass
'''
