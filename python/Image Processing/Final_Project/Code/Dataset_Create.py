import os
from matplotlib.pyplot import box
import numpy as np
import torch
from PIL import Image
import torchvision.transforms as T
import matplotlib.pylab as plt
import cv2


class dataset_create(torch.utils.data.Dataset):
    def __init__(self, imgs, masks):
        self.imgs = imgs
        self.masks = masks


    def __getitem__(self, idx):
        img = self.imgs[idx]
        mask = self.masks[idx]
        img = cv2.resize(img, dsize=(500, 500), interpolation=cv2.INTER_LINEAR)
        mask = cv2.resize(mask, dsize=(500, 500), interpolation=cv2.INTER_LINEAR)
        img = img.transpose((2, 0, 1))
        mask = np.array(mask)

        number_of_object = 1
        masks = (mask > 0) * 1 #obj_ids[:, None, None]   
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
        masks = torch.as_tensor(np.array([masks]), dtype=torch.float32)
        image_id = torch.tensor([idx])
        area = len(np.where(masks == 1)[0]) # (boxes[:, 3] - boxes[:, 1]) * (boxes[:, 2] - boxes[:, 0])
        iscrowd = torch.zeros((number_of_object,), dtype=torch.int64)

        target = {}
        target["boxes"] = boxes
        target["labels"] = labels
        target["masks"] = masks
        target["image_id"] = image_id
        target["area"] = area
        target["iscrowd"] = iscrowd

        return img, target

    def __len__(self):
        return len(self.imgs)