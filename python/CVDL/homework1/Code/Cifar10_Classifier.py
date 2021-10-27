import pickle
import torch
import torch.nn as nn
# from torchsummary import summary
import torchvision
import torchvision.transforms as transforms
import matplotlib.pylab as plt
import numpy as np
from torchvision.models import vgg16
from VGG16_Model import VGG16
import os

class cifar10_classifier():

    def __init__(self):
        self.targetTable = {
             0: "airplane",
             1: "automobile",
             2: "bird",
             3: "cat",
             4: "deer",
             5: "dog",
             6: "frog",
             7: "horse",
             8: "ship",
             9: "truck"
        }


    def plot_Cifa10_images(self):

        transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
        trainset = torchvision.datasets.CIFAR10(root = './dataset', train = True, download = True, transform = transform)
        train_dataloader = torch.utils.data.DataLoader(trainset, batch_size = 1, shuffle = False, num_workers = 2)

        count = 0
        for step, (images, targets) in enumerate(train_dataloader):

            for image, target in zip(images, targets):
                image = image.numpy().transpose((1, 2, 0))

                plt.subplot(331 + count)
                plt.title(self.targetTable[int(target)])
                plt.imshow(image)

                count += 1
                
                if count == 9: break

            if count == 9: break

        plt.show()

    def train_data(self):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")    

        transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

        epoch = 20
        batch_size = 512
        learning_rate = 0.0001

        trainset = torchvision.datasets.CIFAR10(root = './dataset', train = True, download = True, transform = transform)
        train_dataloader = torch.utils.data.DataLoader(trainset, batch_size = batch_size, shuffle = True, num_workers = 2)
        number_of_data = len(trainset)
        number_of_batch = len(train_dataloader)

        # testset = torchvision.datasets.CIFAR10(root = './dataset', train = False, download = True, transform = transform)
        # test_dataloader = torch.utils.data.DataLoader(testset, batch_size = batch_size, shuffle = False, num_workers = 2)
        
        model = VGG16().to(device)

        optimizer = torch.optim.Adam(model.parameters(), lr = learning_rate)  
        loss_func = nn.CrossEntropyLoss().to(device)

        epoch_loss = []
        epoch_accuracy = []
        for step in range(1, epoch + 1):

            total_batch_loss = 0
            correct_predict = 0
            count = 0

            for images, targets in train_dataloader:

                output = model(images.float().to(device))
                optimizer.zero_grad()
                loss = loss_func(output, targets.long().to(device))
                loss.backward()
                optimizer.step()

                _, predict = torch.max(nn.functional.softmax(output, dim = 1), 1)
                correct_predict += (predict.data.cpu() == targets).sum()
                total_batch_loss += loss.data.cpu().numpy()

                print("\r", "Training: %.4f" % ((count / number_of_batch) * 100.), "%", " (loss = {}, epoch: {})".format(loss, step), end=" ")
                count += 1

            epoch_loss += [total_batch_loss / number_of_batch]
            epoch_accuracy += [correct_predict / number_of_data]
            # print("\r", "Training: %.4f" % ((step / epoch) * 100.), "%", " (loss = {}, accuracy = {}, epoch: {})".format(epoch_loss[-1], epoch_accuracy[-1], step), end=" ")

        if not os.path.exists("./model/"):
            os.makedirs("./model/")
        torch.save(model, "./model/model.pkl")

        if not os.path.exists("./predict/"):
            os.makedirs("./predict/")
        np.savez("./predict/loss.npz", data = epoch_loss)
        np.savez("./predict/accuracy.npz", data = epoch_accuracy)


    def plot_result(self, kind = "loss"):

        data = np.load("./predict/{}.npz".format(kind))
        plt.title(kind)
        plt.xlabel("epoch")
        plt.ylabel(kind)
        plt.plot(list(range(1, len(data["data"]) + 1)), data["data"], "-o")
        plt.xticks(list(range(1, len(data["data"]) + 1, 2)))
        plt.show()


        
            

            

        


    