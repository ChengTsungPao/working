import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
from torchsummary import summary
from torchvision.models import vgg16
from VGG16_Model import VGG16

import os
import numpy as np
import matplotlib.pylab as plt

class cifar10_classifier():

    def __init__(self):

        # dataset
        transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
        self.trainset = torchvision.datasets.CIFAR10(root = './dataset', train = True, download = True, transform = transform)
        self.testset = torchvision.datasets.CIFAR10(root = './dataset', train = False, download = True, transform = transform)

        # model
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  
        self.model = VGG16().to(self.device)

        # parameter
        self.epoch = 50
        self.batch_size = 512
        self.learning_rate = 0.0001
        self.momentum = 0.9
        self.optimizer = torch.optim.SGD(self.model.parameters(), lr = self.learning_rate, momentum = self.momentum)
        
        # target or kind
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

        os.system('cls||clear')


    def plot_Cifa10_images(self):
        
        plt.figure(figsize = (8, 6), dpi = 100)
        plt.interactive(True)

        for index in range(9):
            image, target = self.trainset[index]
            image = image.data.numpy().transpose((1, 2, 0))
            image = (image + 1) / 2

            plt.subplot(331 + index)
            plt.title(self.targetTable[int(target)])
            plt.axis('off')
            plt.imshow(image)

        plt.tight_layout()
        plt.show()


    def show_model_summary(self):

        summary(self.model, (3, 32, 32))


    def show_hyperParameters(self):

        print("Batch Size {},\n".format(self.batch_size))
        print(self.optimizer)


    def train_data(self):  

        train_dataloader = torch.utils.data.DataLoader(self.trainset, batch_size = self.batch_size, shuffle = True)
        number_of_train_data = len(self.trainset)
        number_of_train_batch = len(train_dataloader)

        test_dataloader = torch.utils.data.DataLoader(self.testset, batch_size = self.batch_size, shuffle = True)
        number_of_test_data = len(self.testset)
        number_of_test_batch = len(test_dataloader)

        loss_func = nn.CrossEntropyLoss().to(self.device)

        epoch_train_loss, epoch_train_accuracy = [], []
        epoch_test_loss, epoch_test_accuracy = [], []

        for step in range(1, self.epoch + 1):
            
            ######################## training ######################## 

            total_batch_train_loss = 0
            correct_train_predict = 0
            train_count = 0

            for images, targets in train_dataloader:

                output = self.model(images.float().to(self.device))
                self.optimizer.zero_grad()
                loss = loss_func(output, targets.long().to(self.device))
                loss.backward()
                self.optimizer.step()

                _, predict = torch.max(nn.functional.softmax(output, dim = 1), 1)
                correct_train_predict += (predict.data.cpu() == targets).sum()
                total_batch_train_loss += loss.data.cpu().numpy()

                print("\r", "Training: %.4f" % ((train_count / number_of_train_batch) * 100.), "%", " (loss = {}, epoch: {})".format(loss, step), end=" ")
                train_count += 1

            epoch_train_loss += [total_batch_train_loss / number_of_train_batch]
            epoch_train_accuracy += [correct_train_predict / number_of_train_data]
            # print("\r", "Training: %.4f" % ((step / epoch) * 100.), "%", " (loss = {}, accuracy = {}, epoch: {})".format(epoch_loss[-1], epoch_accuracy[-1], step), end=" ")

            ######################## testing ######################## 

            total_batch_test_loss = 0
            correct_test_predict = 0
            test_count = 0

            for images, targets in test_dataloader:
    
                output = self.model(images.float().to(self.device))
                loss = loss_func(output, targets.long().to(self.device))

                _, predict = torch.max(nn.functional.softmax(output, dim = 1), 1)
                correct_test_predict += (predict.data.cpu() == targets).sum()
                total_batch_test_loss += loss.data.cpu().numpy()
                print("\r", "Testing: %.4f" % ((test_count / number_of_test_batch) * 100.), "%", end=" ")
                test_count += 1

            epoch_test_loss += [total_batch_test_loss / number_of_test_batch]
            epoch_test_accuracy += [correct_test_predict / number_of_test_data]

        ######################## save data ######################## 

        if not os.path.exists("./model/"):
            os.makedirs("./model/")
        torch.save(self.model, "./model/model.pkl")

        if not os.path.exists("./predict/"):
            os.makedirs("./predict/")
        np.savez("./predict/loss.npz", train = epoch_train_loss, test = epoch_test_loss)
        np.savez("./predict/accuracy.npz", train = epoch_train_accuracy, test = epoch_test_accuracy)


    def test_data(self, index):

        if index == "":
            index = "1"

        if index.isdigit() == False:
            return

        index = int(index) - 1
        if not 0 <= index < len(self.testset):
            return

        if not os.path.exists("./model/"):
            self.train_data()
        
        model = torch.load("./model/model.pkl", map_location=torch.device(self.device))
        shape = np.shape(self.testset[index][0])

        image, target = self.testset[index]
        output = model(torch.tensor(image.data.numpy().reshape(1, shape[0], shape[1], shape[2])).float().to(self.device))
        output = nn.functional.softmax(output, dim = 1)
        output = output.data.cpu().numpy()

        plt.figure(figsize = (16, 6), dpi = 80)
        plt.interactive(True)

        image = (image + 1) / 2
        plt.subplot(121)
        plt.title(self.targetTable[target])
        plt.axis('off')
        plt.imshow(image.data.numpy().transpose((1, 2, 0)))

        plt.subplot(122)
        plt.title("kind of probability")
        plt.bar(self.targetTable.values(), output[0])
        plt.ylabel("probability")
        plt.tight_layout()
        plt.show()


    def plot_result(self):

        if not os.path.exists("./predict/"):
            self.train_data()

        loss = np.load("./predict/{}.npz".format("loss"))
        accuracy = np.load("./predict/{}.npz".format("accuracy"))

        plt.figure(figsize = (16, 6), dpi = 80)
        plt.interactive(True)

        plt.subplot(121)
        plt.title("loss")
        plt.xlabel("epoch")
        plt.ylabel("loss")
        plt.plot(list(range(1, len(loss["train"]) + 1)), loss["train"], "-o", label = "Training")
        plt.plot(list(range(1, len(loss["test"]) + 1)), loss["test"], "-o", label = "Testing")
        plt.xticks(list(range(1, len(loss["train"]) + 1, 2)))

        plt.subplot(122)
        plt.title("accuracy")
        plt.xlabel("epoch")
        plt.ylabel("accuracy")
        plt.plot(list(range(1, len(accuracy["train"]) + 1)), accuracy["train"], "-o", label = "Training")
        plt.plot(list(range(1, len(accuracy["test"]) + 1)), accuracy["test"], "-o", label = "Testing")
        plt.xticks(list(range(1, len(accuracy["train"]) + 1, 2)))

        plt.legend()
        plt.tight_layout()
        plt.show()
