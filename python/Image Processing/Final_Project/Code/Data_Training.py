from numpy import mod
from numpy.lib.type_check import imag
from torch._C import device
from Data_Transfer import data_transfer
import torchvision
import torch
import numpy as np
from engine import train_one_epoch

class data_training(data_transfer):

    def __init__(self, path):
        super().__init__(path)
        self.device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
        self.train_bounding_box_wider_data()


    def train_bounding_box_wider_data(self):
        self.get_bounding_box_wider_data()
        self.bounding_box_wider_data_transfer()

        EPOCH = 10
        BATCH_SIZE = 4

        model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained = True).to(self.device)
        train_dataloader = torch.utils.data.DataLoader(self.bounding_box_wider_dataset, batch_size = BATCH_SIZE, shuffle = True, num_workers = 1)

        optimizer = torch.optim.SGD(model.parameters(), lr = 0.0001, momentum = 0.9, weight_decay=0.0005)
        scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.1)

        for epoch in range(EPOCH):
            train_one_epoch(model, optimizer, train_dataloader, self.device, epoch, BATCH_SIZE, print_freq = 1)
            scheduler.step()

            # scheduler.step()

            # for step, (images, targets) in enumerate(train_dataloader):

            #     targets = [{key: targets[key][index].to(self.device) for key in targets} for index in range(BATCH_SIZE)]
            #     output = model(images.float().to(self.device), targets)
            #     print(output)


        model.eval()
        x = [torch.rand(3, 500, 500).to(self.device), torch.rand(3, 500, 500).to(self.device)]
        predictions = model(x) 
        print(predictions)
