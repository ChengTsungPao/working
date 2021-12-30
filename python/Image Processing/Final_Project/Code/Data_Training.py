from re import L
from sys import prefix
from matplotlib.pyplot import step
from numpy import mod
from numpy.lib.type_check import imag
from Data_Transfer import data_transfer
import torchvision
import torch
import numpy as np
from Library.engine import train_one_epoch
import os
import cv2
import matplotlib.pylab as plt
from torchsummary import summary

class data_training(data_transfer):

    def __init__(self, path):
        super().__init__(path)
        self.device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
        # self.train_bounding_box_wider_data()
        # self.predict_all_bounding_box_wider_data()
        self.train_bounding_box_narrow_data()
        # self.predict_all_bounding_box_narrow_data()
        # self.train_classifier_data()
        # self.predict_all_classifier_data()


    def train_bounding_box_wider_data(self):
        if self.bounding_box_wider_dataset == []:
            self.get_bounding_box_wider_data()
            self.bounding_box_wider_data_transfer()

        EPOCH = 100
        BATCH_SIZE = 4

        model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained = True).to(self.device)
        train_dataloader = torch.utils.data.DataLoader(self.bounding_box_wider_dataset, batch_size = BATCH_SIZE, shuffle = True, num_workers = 1)

        optimizer = torch.optim.SGD(model.parameters(), lr = 0.0001, momentum = 0.9, weight_decay=0.0005)
        # scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.1)

        for epoch in range(EPOCH):
            train_one_epoch(model, optimizer, train_dataloader, self.device, epoch, BATCH_SIZE, print_freq = 1)
            # scheduler.step()

        model.eval()

        if not os.path.exists("./model/"):
            os.makedirs("./model/")
        torch.save(model, "./model/bounding_box_wider_model.pkl")

        self.predict_all_bounding_box_wider_data()


    def predict_all_bounding_box_wider_data(self):
        if self.bounding_box_wider_data == []:
            self.get_bounding_box_wider_data()

        model = torch.load("./model/bounding_box_wider_model.pkl")

        predict = []
        training_size = 500
        
        for index in range(len(self.bounding_box_wider_data)):
            image = self.bounding_box_wider_data[index]
            origin_shape = image.shape
            image = cv2.resize(image, (training_size, training_size), interpolation=cv2.INTER_LINEAR)

            output = model([torch.tensor(image.transpose((2, 0, 1))).float().to(self.device)])
            x1, y1, x2, y2 = output[0]["boxes"][0].data.cpu().numpy().astype(np.float)
            scaleX, scaleY = origin_shape[1] / training_size, origin_shape[0] / training_size
            predict.append(np.array([x1 * scaleX, y1 * scaleY, x2 * scaleX, y2 * scaleY], int))

        if not os.path.exists("./predict/"):
            os.makedirs("./predict/")

        np.savez("./predict/bounding_box_wider_data_predict.npz", predict = predict, goundTruth = self.bounding_box_wider_target)


    def predict_bounding_box_wider_data(self, index):
        if self.bounding_box_wider_data == []:
            self.get_bounding_box_wider_data()

        result = np.load("./predict/bounding_box_wider_data_predict.npz")

        image, target = self.bounding_box_wider_data[index], self.bounding_box_wider_target[index]

        x1, y1, x2, y2 = result["predict"][index]
        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 4)

        x1, y1, x2, y2 = target
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 4)

        cv2.imshow("image", cv2.resize(image, (image.shape[1] // 2, image.shape[0] // 2), interpolation=cv2.INTER_LINEAR))
        cv2.waitKey()  
        cv2.destroyAllWindows()  


    def train_bounding_box_narrow_data(self):
        if self.bounding_box_narrow_dataset == []:
            self.get_bounding_box_narrow_data()
            self.bounding_box_narrow_data_transfer()

        def create_MaskRCNN_model(num_classes):
            model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=False)

            # get the number of input features for the classifier
            in_features = model.roi_heads.box_predictor.cls_score.in_features

            # replace the pre-trained head with a new one
            model.roi_heads.box_predictor = torchvision.models.detection.faster_rcnn.FastRCNNPredictor(in_features, num_classes)

            # now get the number of input features for the mask classifier
            in_features_mask = model.roi_heads.mask_predictor.conv5_mask.in_channels
            hidden_layer = 256

            # and replace the mask predictor with a new one
            model.roi_heads.mask_predictor = torchvision.models.detection.mask_rcnn.MaskRCNNPredictor(in_features_mask, hidden_layer, num_classes)

            return model

        EPOCH = 30
        BATCH_SIZE = 4

        model = create_MaskRCNN_model(2).to(self.device)
        train_dataloader = torch.utils.data.DataLoader(self.bounding_box_narrow_dataset, batch_size = BATCH_SIZE, shuffle = True, num_workers = 1)

        params = [p for p in model.parameters() if p.requires_grad]
        optimizer = torch.optim.SGD(params, lr = 0.00001, momentum = 0.9, weight_decay=0.0005)
        scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.1)

        for epoch in range(EPOCH):
            train_one_epoch(model, optimizer, train_dataloader, self.device, epoch, BATCH_SIZE, print_freq = 1)
            scheduler.step()

        model.eval()

        if not os.path.exists("./model/"):
            os.makedirs("./model/")
        torch.save(model, "./model/bounding_box_narrow_model.pkl")

        self.predict_all_bounding_box_narrow_data()


    def predict_all_bounding_box_narrow_data(self):
        if self.bounding_box_narrow_data == []:
            self.get_bounding_box_narrow_data()

        model = torch.load("./model/bounding_box_narrow_model.pkl")
        result = np.load("./predict/bounding_box_wider_data_predict.npz")
       
        predict = []
        training_size = 500
        
        for index in range(len(self.bounding_box_narrow_data)):
            x1, y1, x2, y2 = result["predict"][index]
            image = self.bounding_box_narrow_data[index][y1:y2, x1:x2]
            origin_shape = image.shape
            image = cv2.resize(image, (training_size, training_size), interpolation=cv2.INTER_LINEAR)
            output = model([torch.tensor(image.transpose((2, 0, 1))).float().to(self.device)])

            totalImage = np.zeros((origin_shape[0], origin_shape[1]))
            print(output)
            for i in range(len(output[0]["masks"])):
                totalImage += cv2.resize(output[0]["masks"][i].data.cpu().numpy().transpose((1, 2, 0)) * output[0]["scores"][i].data.cpu().numpy(), (origin_shape[1], origin_shape[0]), interpolation=cv2.INTER_LINEAR)
            bestScoreImage = cv2.resize(output[0]["masks"][0].data.cpu().numpy().transpose((1, 2, 0)), (origin_shape[1], origin_shape[0]), interpolation=cv2.INTER_LINEAR)
            plt.imshow(output[0]["masks"][0].data.cpu().numpy().transpose((1, 2, 0)))
            plt.show()
            # plt.subplot(131)
            # plt.imshow(totalImage, cmap="jet")
            # plt.subplot(132)
            # plt.imshow(bestScoreImage, cmap="jet")    
            # plt.subplot(133)
            # plt.imshow(self.bounding_box_narrow_data[index][y1:y2, x1:x2], cmap="binary")
            # plt.get_current_fig_manager().window.showMaximized()
            # plt.show()     

            plt.subplot(221)
            plt.imshow(totalImage, cmap="jet")
            plt.subplot(222)
            plt.imshow(bestScoreImage, cmap="jet")    
            plt.subplot(223)
            plt.imshow(self.bounding_box_narrow_data[index][y1:y2, x1:x2], cmap="binary")
            plt.subplot(224)
            plt.imshow(totalImage > 0.5, cmap="binary")    
            plt.show() 

        if not os.path.exists("./predict/"):
            os.makedirs("./predict/")

        np.savez("./predict/bounding_box_narrow_data_predict.npz", predict = predict, goundTruth = self.bounding_box_narrow_target)


    def train_classifier_data(self):
        if self.classifier_dataset == []:
            self.get_classifier_data()
            self.classifier_data_transfer()

        model = torch.nn.Sequential(
            torchvision.models.resnet50(pretrained=True), 
            torch.nn.ReLU(),
            torch.nn.Linear(1000, 2)
        ).to(self.device)

        EPOCH = 50
        BATCH_SIZE = 4

        train_dataloader = torch.utils.data.DataLoader(self.classifier_dataset, batch_size = BATCH_SIZE, shuffle = True, num_workers = 1)
        number_of_batch = len(train_dataloader)
        number_of_data = len(self.classifier_dataset)

        optimizer = torch.optim.SGD(model.parameters(), lr = 0.0001, momentum = 0.9, weight_decay=0.0005)
        loss_func = torch.nn.CrossEntropyLoss()

        for epoch in range(1, EPOCH + 1):

            correct_predict = 0
            total_batch_loss = 0

            for step, (datas, targets) in enumerate(train_dataloader):

                output = model(datas.float().to(self.device))
                optimizer.zero_grad()
                loss = loss_func(output, targets.long().to(self.device))
                loss.backward()
                optimizer.step()

                _, predict = torch.max(torch.nn.functional.softmax(output, dim = 1), 1)
                correct_predict += (predict.data.cpu() == targets).sum()
                total_batch_loss += loss.data.cpu().numpy()

                print("\r", "Batch of Training: %.4f" % ((step / number_of_batch) * 100.), "%", " (loss = {}, epoch: {})".format(loss, epoch), end=" ")

            print("\n Epoch of Training: %.4f" % ((epoch / EPOCH) * 100.), "%", " (loss = {}, accuracy = {}, epoch: {})\n".format(total_batch_loss / number_of_batch, correct_predict / number_of_data, epoch), end=" ")
            print("====================================================")

        if not os.path.exists("./model/"):
            os.makedirs("./model/")
        torch.save(model, "./model/classifier_model.pkl")

    
    def predict_all_classifier_data(self):
        if self.classifier_data == []:
            self.get_classifier_data()

        model = torch.load("./model/classifier_model.pkl")

        predict = []
        training_size = 500

        for image in self.classifier_data:
            image = cv2.resize(image, (training_size, training_size), interpolation=cv2.INTER_LINEAR)
            output = model(torch.tensor([image.transpose((2, 0, 1))]).float().to(self.device))
            _, pre = torch.max(torch.nn.functional.softmax(output, dim = 1), 1)
            predict.append(pre.data.cpu()[0])

        if not os.path.exists("./predict/"):
            os.makedirs("./predict/")

        np.savez("./predict/classifier.npz", label = np.array(["Fracture", "Normal"]), predict = predict, goundTruth = self.classifier_target)


    def predict_classifier_data(self, index):

        result = np.load("./predict/classifier.npz")

        label = result["label"]
        predict = result["predict"]
        goundTruth = result["goundTruth"]

        print("predict = {}, groundTruth = {}".format(label[predict[index]], label[goundTruth[index]]))


