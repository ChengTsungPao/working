
import torch
torch.__version__
import numpy as np
import matplotlib.pyplot as plt
from torch.autograd import Variable

#Variable
x = Variable(torch.ones(2,2),requires_grad=True)
y = x.mean()
y.backward()
x.grad
x.grad_fn
x.data
y.grad_fn


#1D
x = torch.rand(10)
x.size()
temp = torch.FloatTensor([23,24,24.5,26,27.2,23.0])
temp.size()


#2D
from sklearn.datasets import load_boston
boston = load_boston()
print(boston.data.shape)
boston.feature_names
boston_tensor = torch.from_numpy(boston.data)
boston_tensor.size()
boston_tensor[:2]
boston_tensor[:10,:5]


#3D
from PIL import Image
panda = np.array(Image.open('panda.jpg').resize((224,224)))
panda_tensor = torch.from_numpy(panda)
panda_tensor.size()

plt.subplot(221)
plt.imshow(panda);

sales = torch.FloatTensor([1000.0,323.2,333.4,444.5,1000.0,323.2,333.4,444.5])
sales[:5]
sales[:-5]
plt.subplot(222)
plt.imshow(panda_tensor[:,:,0].numpy());
plt.subplot(223)
plt.imshow(panda_tensor[25:175,60:130,0].numpy());
plt.show()
sales = torch.eye(3,3)
sales[0,1]


#4D
from glob import glob
#Read cat images from disk
data_path='D:/program/vscode_workspace/private/data/dogscats/sample/train/cats/'
cats = glob(data_path+'*.jpg')
print("----------------------------\n",len(cats),type(cats))
#Convert images into numpy arrays
cat_imgs = np.array([np.array(Image.open(cat).resize((224,224))) for cat in
cats[:64]])
cat_imgs = cat_imgs.reshape(-1,224,224,3)
cat_tensors = torch.from_numpy(cat_imgs)
cat_tensors.size()
print(cat_tensors.size(),"\n----------------------------")

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

###########################################################
# ### On GPU

# In[ ]:
from time import perf_counter

a = torch.rand(100,100)
b = torch.rand(100,100)

print("Matrix Size : 100x100")
t=perf_counter()
a.matmul(b)
print("CPU:",perf_counter()-t)
#Time taken : 3.23 s

# In[ ]:

#Move the tensors to GPU

a = a.cuda()
b = b.cuda()

t=perf_counter()
a.matmul(b)
print("GPU:",perf_counter()-t,"\n----------------------------")


#Time taken : 11.2 µs  
###########################################################
# In[ ]:
from time import perf_counter

a = torch.rand(10000,10000)
b = torch.rand(10000,10000)

print("Matrix Size : 10000x10000")
t=perf_counter()
a.matmul(b)
print("CPU:",perf_counter()-t)
#Time taken : 3.23 s


#Move the tensors to GPU

a = a.cuda()
b = b.cuda()

t=perf_counter()
a.matmul(b)
print("GPU:",perf_counter()-t,"\n----------------------------")

#Time taken : 11.2 µs  
###########################################################
import torch.nn as nn
f = nn.Linear(17,1) 