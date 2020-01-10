from glob import glob
import os
import numpy as np
import matplotlib.pyplot as plt
import shutil
from torchvision import transforms, models
import torch
import torch.nn as nn
from torch.autograd import Variable
from torch.optim import lr_scheduler
from torch import optim
from torchvision.datasets import ImageFolder
from torchvision.utils import make_grid
import time

def get_train_data(phase):

    file = np.load((path+'/train/{},{}_train,N={},{}.npz').format(particle_data[0],particle_data[1],particle_data[2],line))

    test_input = []
    test_target = []
    train_input = []
    train_target = []
    
    for i in range(len(phase)):
        test_input += file[kind_of_data[0]][800 + move(phase[i]) : 1000 + move(phase[i])].tolist()
        test_target += file[kind_of_data[1]][800 + move(phase[i]) : 1000 + move(phase[i])].tolist()
        train_input += file[kind_of_data[0]][0 + move(phase[i]) : 800 + move(phase[i])].tolist()
        train_target += file[kind_of_data[1]][0 + move(phase[i]) : 800 + move(phase[i])].tolist()

    test_input = np.array(test_input)
    test_target = np.array(test_target)
    train_input = np.array(train_input)
    train_target = np.array(train_target)

    if(dimension==1 and one_dimension_mode==1):
        test_target = np.where(test_target==classify_phase_test[0],9,test_target)
        test_target = np.where(test_target==classify_phase_test[1],10,test_target)
        test_target = np.where(test_target==classify_phase_test[2],10,test_target)
        test_target = np.where(test_target==classify_phase_test[3],9,test_target)
        train_target = np.where(train_target==classify_phase_test[0],9,train_target)
        train_target = np.where(train_target==classify_phase_test[1],10,train_target)
        train_target = np.where(train_target==classify_phase_test[2],10,train_target)
        train_target = np.where(train_target==classify_phase_test[3],9,train_target)

    return [torch.tensor(test_input  ,dtype=torch.float64),
            torch.tensor(test_target ,dtype=torch.float64),
            torch.tensor(train_input ,dtype=torch.float64),
            torch.tensor(train_target,dtype=torch.float64)]


classify_phase = [5,1]
total_data = get_train_data(classify_phase)
test_data  = TensorDataset(total_data[0],total_data[1])
train_data = TensorDataset(total_data[2],total_data[3])
train_gen = DataLoader(dataset=train_data, batch_size=BATCH_SIZE, shuffle=True, num_workers=2) 
valid_gen = DataLoader(dataset=test_data, batch_size=BATCH_SIZE, shuffle=True, num_workers=2) 

def train_model(model, criterion, optimizer, scheduler,num_epochs = 5):
    # Given training neural network: ResNet18,
    # loss fcn(criterion) : Cross Entropy Loss,
    # optimizer : Stochastic Gradient Descent plus momentum,
    # learning rate adjusting.
    
    since = time.time() # count time
    best_model_wts = model.state_dict() # return parameters of model
    best_acc = 0.0 # record the best accuracy
    
    # run several epochs
    for epoch in range(num_epochs):
        print("Epoch {} / {}".format(epoch,num_epochs - 1))
        print("-" * 30)
        
        # 'phase' means we're doing training or verifing
        for phase in ['train','valid']:
            if phase == 'train':
                scheduler.step() # adjust learning rate
                model.train(True) # do model training
            else:
                model.train(False)
            
            # record loss and correct(n.) of each epoch
            running_loss = 0.0
            running_corrects = 0
            
            loop_count = 0
            
            # iterate over data
            for data in dataloaders[phase]: # dict_, phase is keyword
                
                # data is packed-figures in batches
                inputs, labels = data # tuple,stores figures and labels
                
                # wrap them in Variables, and switch onto cuda if available
                if torch.cuda.is_available():
                    inputs = Variable(inputs.cuda())
                    labels = Variable(labels.cuda())
                else:
                    inputs = Variable(inputs)
                    labels = Variable(labels)
                
                # set parameters to 0
                optimizer.zero_grad()
                
                # forward
                outputs = model(inputs) # possibility, [[cat,dog]]
                
                # Maximum value of output data along axis[1],
                # and its index, which is the prediction of model.
                _, preds = torch.max(outputs.data, 1)
                loss = criterion(outputs, labels)
                
                # If training, backward() & optimize parameters
                if phase == 'train':
                    loss.backward()
                    optimizer.step()
                
                # statistics
                running_loss += loss.item() # sum up the losses of this epoch
                #print(preds,labels)
                running_corrects += (preds == labels).sum().item() # True: += 1
            
            # rate of loss and accuracy
            epoch_loss = running_loss / dataset_sizes[phase]
            epoch_acc = running_corrects / dataset_sizes[phase]
            
            print("{} Loss: {:.4f} Acc: {:.4f}".format(
                    phase, epoch_loss, epoch_acc))
                    # :.4f means 4 decimals of input object
            
            # record best results
            if phase == 'valid' and epoch_acc > best_acc:
                best_acc = epoch_acc
                best_model_wts = model.state_dict()
        
        print('-+' * 20)
    time_elapsed = time.time() - since # record runtime
    print("Training complete in {:.0f}m {:.0f}s".format(
        time_elapsed // 60, time_elapsed % 60),
          "\nBest vaue of Accuracy: {:4f}".format(best_acc))
    
    model.load_state_dict(best_model_wts)
    return model



  # Loss and Optimizer
lr = 1e-3
criterion = nn.CrossEntropyLoss() # loss fcn
optimizer_ft = optim.SGD(model_ft.parameters(),lr = lr,momentum = 0.9)
exp_lr_scheduler = lr_scheduler.StepLR(optimizer_ft,step_size = 7,gamma = 0.1)  
model_ft = models.resnet18(pretrained = True)

# fc: last layer of CNN, in_feature gives the same number
#     of input data.
num_ftrs = model_ft.fc.in_features

# output [P(0),P(1)], representing 'cat' and 'dog'.
model_ft.fc = nn.Linear(num_ftrs, 2)
if torch.cuda.is_available():
    model_ft = model_ft.cuda()

model_ft = train_model(model_ft, criterion, optimizer_ft, exp_lr_scheduler, num_epochs = 2)