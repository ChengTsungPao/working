
import torch
import numpy as np
from PIL import Image
from glob import glob
from torch.utils.data import Dataset
from torch.autograd import Variable
import matplotlib.pyplot as plt

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
'''
x,y = get_data()               # x - represents training data, y - represents target variables
w,b = get_weights()            # w,b - Learnable parameters
for i in range(1000):
    y_pred = simple_network(x) # function which computes wx + b
    loss = loss_fn(y, y_pred)  # calculates sum of the squared differences of y and y_pred
    if i % 50 == 0: 
        print(loss)
    optimize(learning_rate)    # Adjust w,b to minimize the loss

plot_variable(x, y, 'ro')
plot_variable(x, y_pred, label='Fitted line')
plt.legend()
plt.show()
print("---------------------------------------------------")
'''
class DogsAndCatsDataset(Dataset):
    def __init__(self,root_dir,size=(224,224)):
        self.files = glob(root_dir)
        self.size = size
    def __len__(self):
        return len(self.files)
    def __getitem__(self,idx):
        img = np.asarray(Image.open(self.files[idx]).resize(self.size))
        label = self.files[idx].split('/')[-1]
        return img,label

image=DogsAndCatsDataset("D:/program/vscode_workspace/private/data/dogscats/sample/train/cats/*.jpg")
#plt.imshow(image[0][0])
#plt.show()
#print(image[0][1])
from torch.utils.data import Dataset, DataLoader

dataloader = DataLoader(image,batch_size=2,num_workers=2)
#print(type(dataloader))

def main():
    for imgs , labels in dataloader:
        for i in range(len(imgs)):
            plt.subplot(241+i)
            plt.title(labels[i])
            plt.imshow(imgs[i])
        plt.show()
        pass
    

if __name__ == '__main__':
    main()


