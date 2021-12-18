from numpy import mod
from numpy.lib.type_check import imag
from Data_Transfer import data_transfer
import torchvision
import torch
import numpy as np
from engine import train_one_epoch
import os
import cv2

class data_training(data_transfer):

    def __init__(self, path):
        super().__init__(path)
        self.device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
        # self.train_bounding_box_wider_data()
        while True:
            index = int(input("index of image: "))
            self.predict_bounding_box_wider_data(index)


    def train_bounding_box_wider_data(self):
        if self.bounding_box_wider_data == []:
            self.get_bounding_box_wider_data()
            self.bounding_box_wider_data_transfer()

        EPOCH = 50
        BATCH_SIZE = 4

        model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained = True).to(self.device)
        train_dataloader = torch.utils.data.DataLoader(self.bounding_box_wider_dataset, batch_size = BATCH_SIZE, shuffle = True, num_workers = 1)

        optimizer = torch.optim.SGD(model.parameters(), lr = 0.0001, momentum = 0.9, weight_decay=0.0005)
        scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.1)

        for epoch in range(EPOCH):
            train_one_epoch(model, optimizer, train_dataloader, self.device, epoch, BATCH_SIZE, print_freq = 1)
            scheduler.step()

        model.eval()

        if not os.path.exists("./model/"):
            os.makedirs("./model/")
        torch.save(model, "./model/bounding_box_wider_model.pkl")


    def predict_bounding_box_wider_data(self, index):
        if self.bounding_box_wider_data == []:
            self.get_bounding_box_wider_data()
            self.bounding_box_wider_data_transfer()
            
        image, target = self.bounding_box_wider_data[index], self.bounding_box_wider_target[index]
        origin_shape = image.shape
        image = cv2.resize(image, (500, 500), interpolation=cv2.INTER_LINEAR)

        model = torch.load("./model/bounding_box_wider_model.pkl")
        predict = model([torch.tensor(image.transpose((2, 0, 1))).float().to(self.device)])

        x1, y1, x2, y2 = predict[0]["boxes"][0].data.cpu().numpy().astype(np.int32)
        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 1)
        image = cv2.resize(image, (origin_shape[1], origin_shape[0]), interpolation=cv2.INTER_LINEAR)

        x1, y1, x2, y2 = target
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 4)
        image = cv2.resize(image, (image.shape[1] // 2, image.shape[0] // 2), interpolation=cv2.INTER_LINEAR)

        cv2.imshow("image", image)
        cv2.waitKey()  
        cv2.destroyAllWindows()  

