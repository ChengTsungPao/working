import torch
import torch.nn as nn
import torchvision.models as models

import torch
import torch.nn as nn

class VGG16(nn.Module):
    def __init__(self, num_classes = 10):
        super(VGG16, self).__init__()
        self.vgg16 = models.vgg16_bn(pretrained=True)
        self.vgg16.avgpool = nn.Sequential()
        self.vgg16.classifier = nn.Sequential(
            nn.Linear(512, 4096),
            nn.ReLU(),
            nn.Linear(4096, 4096),
            nn.ReLU(),
            nn.Linear(4096, num_classes)
        )

    def forward(self, x):
        return self.vgg16(x)

# class VGG16(nn.Module):
    
#     def __init__(self, num_classes = 10):
#         super(VGG16, self).__init__()

#         self.block_1 = nn.Sequential(
#             nn.Conv2d(in_channels=3, out_channels=64, kernel_size=(3, 3), stride=(1, 1), padding=1),
#             nn.BatchNorm2d(64),
#             nn.ReLU(),
#             nn.Conv2d(in_channels=64, out_channels=64, kernel_size=(3, 3), stride=(1, 1), padding=1),
#             nn.BatchNorm2d(64),
#             nn.ReLU(),
#             nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2))
#         )

#         self.block_2 = nn.Sequential(
#             nn.Conv2d(in_channels=64, out_channels=128, kernel_size=(3, 3), stride=(1, 1), padding=1),
#             nn.BatchNorm2d(128),
#             nn.ReLU(),
#             nn.Conv2d(in_channels=128, out_channels=128, kernel_size=(3, 3), stride=(1, 1), padding=1),
#             nn.BatchNorm2d(128),
#             nn.ReLU(),
#             nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2))
#         )
        
#         self.block_3 = nn.Sequential(
#             nn.Conv2d(in_channels=128, out_channels=256, kernel_size=(3, 3), stride=(1, 1), padding=1),
#             nn.BatchNorm2d(256),
#             nn.ReLU(),
#             nn.Conv2d(in_channels=256, out_channels=256, kernel_size=(3, 3), stride=(1, 1), padding=1),
#             nn.BatchNorm2d(256),
#             nn.ReLU(),
#             nn.Conv2d(in_channels=256, out_channels=256, kernel_size=(3, 3), stride=(1, 1), padding=1),
#             nn.BatchNorm2d(256),
#             nn.ReLU(),
#             nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2))
#         )

#         self.block_4 = nn.Sequential(
#             nn.Conv2d(in_channels=256, out_channels=512, kernel_size=(3, 3), stride=(1, 1), padding=1),
#             nn.BatchNorm2d(512),
#             nn.ReLU(),
#             nn.Conv2d(in_channels=512, out_channels=512, kernel_size=(3, 3), stride=(1, 1), padding=1),
#             nn.BatchNorm2d(512),
#             nn.ReLU(),
#             nn.Conv2d(in_channels=512, out_channels=512, kernel_size=(3, 3), stride=(1, 1), padding=1),
#             nn.BatchNorm2d(512),
#             nn.ReLU(),
#             nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2))
#         )

#         self.block_5 = nn.Sequential(
#             nn.Conv2d(in_channels=512, out_channels=512, kernel_size=(3, 3), stride=(1, 1), padding=1),
#             nn.BatchNorm2d(512),
#             nn.ReLU(),
#             nn.Conv2d(in_channels=512, out_channels=512, kernel_size=(3, 3), stride=(1, 1), padding=1),
#             nn.BatchNorm2d(512),
#             nn.ReLU(),
#             nn.Conv2d(in_channels=512, out_channels=512, kernel_size=(3, 3), stride=(1, 1), padding=1),
#             nn.BatchNorm2d(512),
#             nn.ReLU(),
#             nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2))
#         )

#         self.classifier = nn.Sequential(
#             nn.Linear(512, 4096),
#             nn.ReLU(),
#             nn.Linear(4096, 4096),
#             nn.ReLU(),
#             nn.Linear(4096, num_classes),
#         )

#     def forward(self, x):

#         x = self.block_1(x)
#         x = self.block_2(x)
#         x = self.block_3(x)
#         x = self.block_4(x)
#         x = self.block_5(x)
#         x = x.view(x.size(0), -1)
#         output = self.classifier(x)
#         # output = nn.functional.softmax(output , dim=1)

#         return output


