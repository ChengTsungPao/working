
# coding: utf-8 

# In[1]:


from glob import glob
import os
import numpy as np
import matplotlib.pyplot as plt
import shutil
from torchvision import transforms
from torchvision import models
import torch
from torch.autograd import Variable
import torch.nn as nn
from torch.optim import lr_scheduler
from torch import optim
from torchvision.datasets import ImageFolder
from torchvision.utils import make_grid
import time
#get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


def imshow(inp):
    """Imshow for Tensor."""
    inp = inp.numpy().transpose((1, 2, 0))
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    inp = std * inp + mean
    inp = np.clip(inp, 0, 1)
    plt.imshow(inp)


# ## Peep look into the downloaded data 

# ```
#     chapter3/
#         dogsandcats/
#             train/
#                 dog.183.jpg
#                 cat.2.jpg
#                 cat.17.jpg
#                 dog.186.jpg
#                 cat.27.jpg
#                 dog.193.jpg
#   
# 
# ```
# 
# ```
#     chapter3/
#         dogsandcats/
#             train/
#                 dog/
#                     dog.183.jpg
#                     dog.186.jpg
#                     dog.193.jpg
#                 cat/
#                     cat.17.jpg
#                     cat.2.jpg
#                     cat.27.jpg
#             valid/
#                 dog/
#                     dog.173.jpg
#                     dog.156.jpg
#                     dog.123.jpg
#                 cat/
#                     cat.172.jpg
#                     cat.20.jpg
#                     cat.21.jpg
# 
# ```
# 
# 

# ## Create validation data set

# In[3]:


#path = '../Chapter03/dogs-vs-cats/train/'
path = '../data/dogs-vs-cats/'


# In[4]:


files = glob(os.path.join(path,'*/*.jpg'))


# In[23]:


files[0].split('\\')[-1].split('.')


# In[24]:


files[0].split('\\')[-1]


# In[14]:


print(f'Total no of images {len(files)}')


# In[15]:


no_of_images = len(files)


# In[16]:


no_of_images*0.8


# In[17]:


shuffle = np.random.permutation(no_of_images)


# In[18]:


os.mkdir(os.path.join(path,'valid'))


# In[19]:


for t in ['train','valid']:
    for folder in ['dog/','cat/']:
        os.mkdir(os.path.join(path,t,folder)) 


# In[25]:


for i in shuffle[:5000]:
    #shutil.copyfile(files[i],'../chapter3/dogsandcats/valid/')
    folder = files[i].split('\\')[-1].split('.')[0]
    image = files[i].split('\\')[-1]
    os.rename(files[i],os.path.join(path,'valid',folder,image))


# In[26]:


for i in shuffle[5000:]:
    #shutil.copyfile(files[i],'../chapter3/dogsandcats/valid/')
    folder = files[i].split('\\')[-1].split('.')[0]
    image = files[i].split('\\')[-1]
    os.rename(files[i],os.path.join(path,'train',folder,image))


# ## Check if GPU is present

# In[7]:


if torch.cuda.is_available():
    is_cuda = True


# ## Load data into PyTorch tensors

# In[8]:


simple_transform = transforms.Compose([transforms.Resize((224,224))
                                       ,transforms.ToTensor()
                                       ,transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])
train = ImageFolder('../data/dogs-vs-cats/train/',simple_transform)
valid = ImageFolder('../data/dogs-vs-cats/valid/',simple_transform)


# In[9]:


print(train.class_to_idx)
print(train.classes)


# In[10]:


imshow(train[50][0])


# ## Create data generators

# In[11]:


train_data_gen = torch.utils.data.DataLoader(train, shuffle=True,batch_size=32, num_workers=1)
valid_data_gen = torch.utils.data.DataLoader(valid, batch_size=32, num_workers=1)


# In[12]:


dataset_sizes = {'train':len(train_data_gen.dataset), 'valid':len(valid_data_gen.dataset)}


# In[13]:


dataset_sizes


# In[14]:


dataloaders = {'train':train_data_gen, 'valid':valid_data_gen}


# ## Create a network

# In[15]:


model_ft = models.resnet18(pretrained=True)
num_ftrs = model_ft.fc.in_features
model_ft.fc = nn.Linear(num_ftrs, 2)

if torch.cuda.is_available():
    model_ft = model_ft.cuda()


# In[16]:


print(model_ft)


# In[17]:


# Loss and Optimizer
lr = 1e-3
criterion = nn.CrossEntropyLoss()
optimizer_ft = optim.SGD(model_ft.parameters(), lr=lr, momentum=0.9)
exp_lr_scheduler = lr_scheduler.StepLR(optimizer_ft, step_size=7, gamma=0.1)


# In[18]:


def train_model(model, criterion, optimizer, scheduler, num_epochs=5):
    since = time.time()

    best_model_wts = model.state_dict()
    best_acc = 0.0

    for epoch in range(num_epochs):
        print('Epoch {}/{}'.format(epoch, num_epochs - 1))
        print('-' * 10)

        # Each epoch has a training and validation phase
        for phase in ['train', 'valid']:
            if phase == 'train':
                scheduler.step()
                model.train(True)  # Set model to training mode
            else:
                model.train(False)  # Set model to evaluate mode

            running_loss = 0.0
            running_corrects = 0

            # Iterate over data.
            for data in dataloaders[phase]:
                # get the inputs
                inputs, labels = data

                # wrap them in Variable
                if torch.cuda.is_available():
                    inputs = Variable(inputs.cuda())
                    labels = Variable(labels.cuda())
                else:
                    inputs, labels = Variable(inputs), Variable(labels)

                # zero the parameter gradients
                optimizer.zero_grad()
                
                # forward
                outputs = model(inputs)
                _, preds = torch.max(outputs.data, 1)
                loss = criterion(outputs, labels)

                # backward + optimize only if in training phase
                if phase == 'train':
                    loss.backward()
                    optimizer.step()

                # statistics
                running_loss += loss.item()
                running_corrects += (preds == labels).sum().item()
                

            epoch_loss = running_loss / dataset_sizes[phase]
            epoch_acc = running_corrects / dataset_sizes[phase]

            print('{} Loss: {:.4f} Acc: {:.4f}'.format(phase, epoch_loss, epoch_acc))

            # deep copy the model
            if phase == 'valid' and epoch_acc > best_acc:
                best_acc = epoch_acc
                best_model_wts = model.state_dict()

        print()

    time_elapsed = time.time() - since
    print('Training complete in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))
    print('Best val Acc: {:4f}'.format(best_acc))

    # load best model weights
    model.load_state_dict(best_model_wts)
    return model


# In[19]:


model_ft = train_model(model_ft, criterion, optimizer_ft, exp_lr_scheduler, num_epochs=2)

