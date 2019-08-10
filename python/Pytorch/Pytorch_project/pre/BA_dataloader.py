# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 15:46:09 2019

@author: user
"""

import numpy as np
import torch
from torch.utils.data import DataLoader, TensorDataset
from glob import glob

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
N_batch = 8

for size in list(full_data_set.keys()):
    for work in ['train','test']:
        tensor_data[size + work]=[        
            DataLoader(dataset = TensorDataset(torch.tensor(full_data_set[size][work]['BA'],
                                                                        dtype = torch.float64),
                                               torch.tensor(full_data_set[size][work]['phase'],
                                                                          dtype = torch.float64)),
                       batch_size=N_batch,
                       shuffle=True,
                       num_workers=2) ]







