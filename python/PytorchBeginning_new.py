
# coding: utf-8

# In[1]:


import torch
torch.__version__ 


# In[2]:


import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

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

def plot_variable(x,y,z='',**kwargs): # **kwargs為dic的形式，可與*args比較
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


# ## Training

# In[4]:


x,y = get_data()               # x - represents training data, y - represents target variables
w,b = get_weights()            # w,b - Learnable parameters
for i in range(1000):
    y_pred = simple_network(x) # function which computes wx + b
    loss = loss_fn(y, y_pred)  # calculates sum of the squared differences of y and y_pred
    if i % 50 == 0: 
        print(loss)
    optimize(learning_rate)    # Adjust w,b to minimize the loss


# In[5]:


#x_numpy = x.data.numpy()
plot_variable(x, y, 'ro')
plot_variable(x, y_pred, label='Fitted line')


# ## Tensor introduction

# ### Scalar
# 
# 大小:1x10

# In[6]:


x = torch.rand(10)
x.size()


# ### Vector
# 
# 將torch的變數用浮點數表示

# In[7]:


temp = torch.FloatTensor([23,24,24.5,26,27.2,23.0])
temp.size()


# ### Matrix
# 
# 二維tensor張量的例子

# In[8]:


from sklearn.datasets import load_boston
boston = load_boston()
print(boston.data.shape)


# In[9]:


boston.feature_names


# In[10]:


boston_tensor = torch.from_numpy(boston.data)
boston_tensor.size()


# In[11]:


boston_tensor[:2]


# In[12]:


boston_tensor[:10,:5]


# ### 3d- tensor
# 
# 三維tensor張量的例子

# In[13]:


from PIL import Image

panda = np.array(Image.open('panda.jpg').resize((224,224)))
panda_tensor = torch.from_numpy(panda)
panda_tensor.size()


# In[14]:


plt.imshow(panda);


# ### Slicing Tensor

# In[15]:


sales = torch.FloatTensor([1000.0,323.2,333.4,444.5,1000.0,323.2,333.4,444.5])


# In[16]:


sales[:5]


# In[17]:


sales[:-5] #與 sales[:-4] 相同


# In[18]:


plt.imshow(panda_tensor[:,:,0].numpy());


# In[19]:


plt.imshow(panda_tensor[25:175,60:130,0].numpy());


# ### Select specific element of tensor
# 
# 建立一個tensor形式的單位矩陣

# In[20]:


#torch.eye(shape) produces an diagonal matrix with 1 as it diagonal #elements.
sales = torch.eye(3,3)
sales[0,1]


# ### 4D Tensor
# 
# 抓取一些貓的圖作為四維的陣列

# In[21]:


from glob import glob
#Read cat images from disk
data_path='D:/program/vscode_workspace/private/data/dogscats/sample/train/cats/'
cats = glob(data_path+'*.jpg')
#Convert images into numpy arrays
cat_imgs = np.array([np.array(Image.open(cat).resize((224,224))) for cat in
cats[:64]])
cat_imgs = cat_imgs.reshape(-1,224,224,3)
cat_tensors = torch.from_numpy(cat_imgs)
cat_tensors.size()


# ### Tensor addition and multiplication
# 
# tensor的一些基本運算

# In[22]:


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
# 
# 與cpu比較運算速度

# In[23]:


a = torch.rand(10000,10000)
b = torch.rand(10000,10000)

a.matmul(b)
#Time taken : 3.23 s


# In[24]:


#Move the tensors to GPU
a = a.cuda()
b = b.cuda()
a.matmul(b)
#Time taken : 11.2 µs  


# ### Variables
# 
# 一種包含tensor和gradient的資料類別
# 
# .data——獲得該節點的值，即Tensor類型的值
# 
# .grad——獲得該節點處的梯度信息

# In[25]:


from torch.autograd import Variable
x = Variable(torch.ones(2,2),requires_grad=True)
y = x.mean()
y.backward()
x.grad


# In[26]:


x.grad_fn


# In[27]:


x.data


# In[28]:


y.grad_fn


# ### Create data for our neural network
# 
# 創建原始data並用Variable的形式表達
# 

# In[29]:


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
# 
# 初始化原本的weight和bais

# In[30]:


def get_weights():
    w = Variable(torch.randn(1),requires_grad = True)
    b = Variable(torch.randn(1),requires_grad=True)
    return w,b


# ### Implement Neural Network
# 
# 神經網路層與層之間聯繫的基本公式

# In[31]:


def simple_network(x):
    y_pred = torch.matmul(x,w)+b
    return y_pred


# ### Implement Neural Network in Pytorch
# 
# 建立神經層的基本方式(例如:CNN中會用到的max pooling)
# 
# https://pytorch.org/docs/stable/nn.html

# In[32]:


import torch.nn as nn
f = nn.Linear(17,1) # Much simpler.
f


# ### Implementing Loss Function
# 
# lossfunction的運算方式，類似tensorflow中的loss = tf.reduce_mean(tf.square(y-y_data))

# In[33]:


def loss_fn(y,y_pred):
    loss = (y_pred-y).pow(2).sum()
    for param in [w,b]:
        if not param.grad is None: param.grad.data.zero_()
    loss.backward()
    return loss.data[0]


# ### Implementing Optimizer
# 
# 定義優化器，並調整優化器的訓練效率

# In[34]:


def optimize(learning_rate):
    w.data -= learning_rate * w.grad.data
    b.data -= learning_rate * b.grad.data


# ## Loading Data

# ### Defining Dataset
# 
# 利用類別的方式彙整圖形數據
# 
# _init_:為初始化所有的物件
# 
# _len_:物件的資料項目
# 
# _getitem_:傳回物件中的資料項目的第k資料

# In[35]:


from torch.utils.data import Dataset
class DogsAndCatsDataset(Dataset):
    def __init__(self,):
        pass
    def __len__(self):
        pass
    def __getitem__(self,idx):
        pass


# In[36]:


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
    
image=DogsAndCatsDataset("D:/program/vscode_workspace/private/data/dogscats/sample/train/cats/*.jpg")
print(len(image))
print(image.size)
print(image[0][1])
print(image)


# ### Defining DataLoader to iterate over Dogs and Cats Dataset

# In[37]:


from torch.utils.data import Dataset, DataLoader

dataloader = DataLoader(DogsAndCatsDataset,batch_size=32,num_workers=2)
for imgs , labels in dataloader:
        #Apply your DL on the dataset.
    pass

