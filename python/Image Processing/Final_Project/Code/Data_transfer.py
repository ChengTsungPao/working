from Data_Reader import data_reader
import numpy as np
import torch

class data_transfer(data_reader):

    def __init__(self, path):
        super().__init__(path)


    # def bounding_box_wider_data_transfer(self):
    #     boxes = []
    #     for i in range(num_objs):
    #         pos = np.where(masks[i])
    #         xmin = np.min(pos[1])
    #         xmax = np.max(pos[1])
    #         ymin = np.min(pos[0])
    #         ymax = np.max(pos[0])
    #         boxes.append([xmin, ymin, xmax, ymax])

    #     # convert everything into a torch.Tensor
    #     boxes = torch.as_tensor(boxes, dtype=torch.float32)
    #     # there is only one class
    #     labels = torch.ones((num_objs,), dtype=torch.int64)
    #     masks = torch.as_tensor(masks, dtype=torch.uint8)

    #     image_id = torch.tensor([idx])
    #     area = (boxes[:, 3] - boxes[:, 1]) * (boxes[:, 2] - boxes[:, 0])
    #     # suppose all instances are not crowd
    #     iscrowd = torch.zeros((num_objs,), dtype=torch.int64)

    #     target = {}
    #     target["boxes"] = boxes
    #     target["labels"] = labels
    #     target["masks"] = masks
    #     target["image_id"] = image_id
    #     target["area"] = area
    #     target["iscrowd"] = iscrowd

    #     if self.transforms is not None:
    #         img, target = self.transforms(img, target)
