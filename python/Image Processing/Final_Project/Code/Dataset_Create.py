import os
from matplotlib.pyplot import box
import numpy as np
import torch
from PIL import Image
import torchvision.transforms as T
import matplotlib.pylab as plt
import cv2
from torchvision import transforms

class dataset_create(torch.utils.data.Dataset):
    def __init__(self, imgs, masks, training_size):
        self.imgs = imgs
        self.masks = masks
        self.training_size = training_size
        self.transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomVerticalFlip(p=0.5),
            transforms.ColorJitter()
        ])


    def __getitem__(self, idx):
        img = self.imgs[idx]
        mask = self.masks[idx]
        img = cv2.resize(img, dsize=(self.training_size, self.training_size), interpolation=cv2.INTER_LINEAR)
        mask = cv2.resize(mask, dsize=(self.training_size, self.training_size), interpolation=cv2.INTER_LINEAR)
        img = img.transpose((2, 0, 1))
        mask = np.array(mask)

        number_of_object = 1
        masks = mask > 0 #obj_ids[:, None, None]   
        # plt.subplot(121)
        # plt.imshow(img.transpose((1, 2, 0)), cmap="binary")
        # plt.subplot(122)
        # plt.imshow(masks, cmap="binary")
        # plt.show()
   
        boxes = []
        pos = np.where(masks)
        xmin = np.min(pos[1])
        xmax = np.max(pos[1])
        ymin = np.min(pos[0])
        ymax = np.max(pos[0])
        boxes.append([xmin, ymin, xmax, ymax])

        # convert everything into a torch.Tensor
        boxes = torch.as_tensor(boxes, dtype=torch.float32)
        labels = torch.ones((number_of_object,), dtype=torch.int64)
        masks = torch.as_tensor(np.array([masks]), dtype=torch.uint8)
        image_id = torch.tensor([idx])
        area = (boxes[:, 3] - boxes[:, 1]) * (boxes[:, 2] - boxes[:, 0]) # len(np.where(masks == 1)[0])
        iscrowd = torch.zeros((number_of_object,), dtype=torch.int64)

        target = {}
        target["boxes"] = boxes
        target["labels"] = labels
        target["masks"] = masks
        target["image_id"] = image_id
        target["area"] = area
        target["iscrowd"] = iscrowd

        img = self.transform(img)
        img = np.array(img)
        img = img.transpose(1, 2, 0)

        return img, target


    def __len__(self):
        return len(self.imgs)