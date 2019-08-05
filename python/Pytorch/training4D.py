import torch
import torch.nn as nn
import torch.utils.data as Data

class CNN(nn.Module):
    def __init__(self,conv1,conv2,linear):
        super(CNN, self).__init__()
        self.conv1 = nn.Sequential(
            nn.Conv3d(conv1[0],conv1[1],kernel_size=conv1[2],stride=conv1[3],padding=conv1[4]),
            nn.ReLU(),
            nn.MaxPool3d(kernel_size=(1,2,2),stride=(1,2,2))
            )
        self.conv2 = nn.Sequential(
            nn.Conv3d(conv2[0],conv2[1],kernel_size=conv2[2],stride=conv2[3],padding=conv2[4]),
            nn.ReLU(),
            nn.MaxPool3d(kernel_size=(2,2,2),stride=(2,2,2))
            )
        self.out = nn.Linear(linear[0], linear[1])   # fully connected layer, output 10 classes

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = x.view(x.size(0), -1)   # 展平多维的卷积图成 (batch_size, 32 * 7 * 7)
        output = self.out(x)
        return output

cnn = CNN((3, 16, (3,3,3), 1, (1,1,1)),(64, 128, (3,3,3), 1, (1,1,1)),(32 * 7 * 7, 2))

EPOCH = 1           # 训练整批数据多少次, 为了节约时间, 我们只训练一次
BATCH_SIZE = 50
LR = 0.001  
train_loader = Data.DataLoader(dataset=train_data, batch_size=BATCH_SIZE, shuffle=True)
optimizer = torch.optim.Adam(cnn.parameters(), lr=LR)   # optimize all cnn parameters
loss_func = nn.CrossEntropyLoss()   # the target label is not one-hotted
        # 学习率

# training and testing
for epoch in range(EPOCH):
    for step, (b_x, b_y) in enumerate(train_loader):   # 分配 batch data, normalize x when iterate train_loader
        output = cnn(b_x)               # cnn output
        loss = loss_func(output, b_y)   # cross entropy loss
        optimizer.zero_grad()           # clear gradients for this training step
        loss.backward()                 # backpropagation, compute gradients
        optimizer.step()                # apply gradients


