

# class ResNet50(nn.Module):
#     def __init__(self, num_classes = 10):
#         super(ResNet50, self).__init__()
#         self.vgg16 = models.vgg16(pretrained=True)
#         self.vgg16.classifier = nn.Sequential(
#             nn.Linear(7 * 7 * 512, 512),
#             nn.ReLU(True),
#             nn.Linear(512, 128),
#             nn.ReLU(True),
#             nn.Linear(128, num_classes)
#         )

#     def forward(self, x):
#         return self.vgg16(x)
