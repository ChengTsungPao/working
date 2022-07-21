import os
import torch
import numpy as np
from torch.autograd import Variable
from torchsummary import summary
from net.sanet import SANet
from config import config

# os.environ['CUDA_VISIBLE_DEVICES'] = '0'

use_gpu_or_not = True
device = torch.device("cuda" if use_gpu_or_not else "cpu")

model = SANet(config)

checkpoint = torch.load("./results/model/model.ckpt")
model.load_state_dict(checkpoint['state_dict'])
model = torch.nn.DataParallel(model, device_ids = [0])
model = model.module.to(device)

model.set_mode('eval')

inputs = Variable(torch.rand([1, 1,128,128,128])).to(device)

# truth_bboxes = np.array([
#     [[ 44.5, 242.5, 144.,  10., 18.,  17. ]]
# ])

# truth_labels = np.array([
#     [1.]
# ])
model.forward(inputs, None, None)
detections = model.rpn_proposals.cpu().numpy()
print(detections)