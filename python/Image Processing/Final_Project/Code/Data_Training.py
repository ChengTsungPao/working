from Data_Transfer import data_transfer
from Config import wider_data_training_size, narrow_data_training_size, classifier_data_training_size
from Config import imageTempFolder, wider_data_image_filename, wider_data_result_filename, narrow_data_image_filename, narrow_data_result_filename, grad_cam_result_filename
from Config import wider_data_model, narrow_data_model, classifier_data_model
import torchvision
import torch
import numpy as np
from Library.engine import train_one_epoch, evaluate
import os
import cv2
import copy

from pytorch_grad_cam import GradCAM, grad_cam
from pytorch_grad_cam.utils.image import show_cam_on_image

class data_training(data_transfer):

    def __init__(self, path):
        super().__init__(path)
        self.device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

        # self.train_bounding_box_wider_data()
        # self.train_bounding_box_narrow_data()
        # self.train_classifier_data()

    ########################################################################################################################################################
    ##################################################### train_bounding_box_wider_data ####################################################################
    ########################################################################################################################################################

    def train_bounding_box_wider_data(self):
        if self.bounding_box_wider_dataset1 == []:
            self.get_bounding_box_wider_data()
            self.bounding_box_wider_data_transfer()

        EPOCH = 100
        BATCH_SIZE = 4

        train_dataloader1 = torch.utils.data.DataLoader(self.bounding_box_wider_dataset1, batch_size = BATCH_SIZE, shuffle = True, num_workers = 1)
        train_dataloader2 = torch.utils.data.DataLoader(self.bounding_box_wider_dataset2, batch_size = BATCH_SIZE, shuffle = True, num_workers = 1)
        train_dataloader3 = torch.utils.data.DataLoader(self.bounding_box_wider_dataset3, batch_size = BATCH_SIZE, shuffle = True, num_workers = 1)

        def train_three_fold_data(dataloader1, dataloader2, dataloader3, nameIndex):

            model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained = True).to(self.device)
            optimizer = torch.optim.SGD(model.parameters(), lr = 0.00001, momentum = 0.9, weight_decay=0.0005)

            for epoch in range(1, EPOCH + 1):
                train_one_epoch(model, optimizer, dataloader1, self.device, epoch, BATCH_SIZE, print_freq = 1)
                train_one_epoch(model, optimizer, dataloader2, self.device, epoch, BATCH_SIZE, print_freq = 1)
                evaluate(model, dataloader3, self.device)

            model.eval()

            if not os.path.exists("./model/"):
                os.makedirs("./model/")
            torch.save(model, "./model/bounding_box_wider_model{}.pkl".format(nameIndex))

        def train_all_data():

            model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained = True).to(self.device)
            optimizer = torch.optim.SGD(model.parameters(), lr = 0.00001, momentum = 0.9, weight_decay=0.0005)

            for epoch in range(1, EPOCH + 1):
                train_one_epoch(model, optimizer, train_dataloader1, self.device, epoch, BATCH_SIZE, print_freq = 1)
                train_one_epoch(model, optimizer, train_dataloader2, self.device, epoch, BATCH_SIZE, print_freq = 1)
                train_one_epoch(model, optimizer, train_dataloader3, self.device, epoch, BATCH_SIZE, print_freq = 1)

            model.eval()

            if not os.path.exists("./model/"):
                os.makedirs("./model/")
            torch.save(model, "./model/bounding_box_wider_model.pkl")

        train_three_fold_data(train_dataloader1, train_dataloader2, train_dataloader3, 1)
        train_three_fold_data(train_dataloader2, train_dataloader3, train_dataloader1, 2)
        train_three_fold_data(train_dataloader1, train_dataloader3, train_dataloader2, 3)
        # train_all_data()


    def predict_all_bounding_box_wider_data(self):
        if self.bounding_box_wider_data == []:
            self.get_bounding_box_wider_data()

        if torch.cuda.is_available():
            model = torch.load("./model/{}".format(wider_data_model))
        else:
            model = torch.load("./model/{}".format(wider_data_model), map_location=torch.device('cpu'))

        predict = []
        
        for index in range(len(self.bounding_box_wider_data)):
            image = self.bounding_box_wider_data[index]
            origin_shape = image.shape
            image = cv2.resize(image, (wider_data_training_size, wider_data_training_size), interpolation=cv2.INTER_LINEAR)
            output = model([torch.tensor(image.transpose((2, 0, 1))).float().to(self.device)])
            if len(output[0]["boxes"]) == 0:
                predict.append(np.array([0, 0, 1, 1], int))
                continue
            
            x1, y1, x2, y2 = output[0]["boxes"][0].data.cpu().numpy().astype(np.float)
            scaleX, scaleY = origin_shape[1] / wider_data_training_size, origin_shape[0] / wider_data_training_size
            predict.append(np.array([x1 * scaleX, y1 * scaleY, x2 * scaleX, y2 * scaleY], int))

        if not os.path.exists("./predict/"):
            os.makedirs("./predict/")

        np.savez("./predict/bounding_box_wider_data_predict.npz", predict = predict, goundTruth = self.bounding_box_wider_target)


    def predict_bounding_box_wider_data(self, index):
        if self.bounding_box_wider_data == []:
            self.get_bounding_box_wider_data()

        result = np.load("./predict/bounding_box_wider_data_predict.npz", allow_pickle = True)

        image, target = copy.deepcopy(self.bounding_box_wider_data[index]), self.bounding_box_wider_target[index]
        cv2.imwrite(imageTempFolder + wider_data_image_filename, image)

        x1, y1, x2, y2 = target
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 4)

        x1, y1, x2, y2 = result["predict"][index]
        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 4)

        cv2.imwrite(imageTempFolder + wider_data_result_filename, image)
        cv2.imwrite(imageTempFolder + narrow_data_image_filename, copy.deepcopy(self.bounding_box_wider_data[index])[y1:y2, x1:x2])
        # cv2.imshow("wider_data_image", cv2.resize(image, (image.shape[1] // 2, image.shape[0] // 2), interpolation=cv2.INTER_LINEAR))
        # cv2.waitKey()  
        # cv2.destroyAllWindows() 
        
    ########################################################################################################################################################
    ######################################################## train_bounding_box_narrow_data ################################################################
    ########################################################################################################################################################

    def train_bounding_box_narrow_data(self):
        if self.bounding_box_narrow_dataset1 == []:
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

        EPOCH = 500
        BATCH_SIZE = 4

        train_dataloader1 = torch.utils.data.DataLoader(self.bounding_box_narrow_dataset1, batch_size = BATCH_SIZE, shuffle = True, num_workers = 1)
        train_dataloader2 = torch.utils.data.DataLoader(self.bounding_box_narrow_dataset2, batch_size = BATCH_SIZE, shuffle = True, num_workers = 1)
        train_dataloader3 = torch.utils.data.DataLoader(self.bounding_box_narrow_dataset3, batch_size = BATCH_SIZE, shuffle = True, num_workers = 1)

        def train_three_fold_data(dataloader1, dataloader2, dataloader3, nameIndex):

            model = create_MaskRCNN_model(2).to(self.device)
            optimizer = torch.optim.SGD(model.parameters(), lr = 0.00001, momentum = 0.9)

            for epoch in range(1, EPOCH + 1):
                train_one_epoch(model, optimizer, dataloader1, self.device, epoch, BATCH_SIZE, print_freq = 1)
                train_one_epoch(model, optimizer, dataloader2, self.device, epoch, BATCH_SIZE, print_freq = 1)
                evaluate(model, dataloader3, self.device)

            model.eval()

            if not os.path.exists("./model/"):
                os.makedirs("./model/")
            torch.save(model, "./model/bounding_box_narrow_model{}.pkl".format(nameIndex))

        def train_all_data():

            model = create_MaskRCNN_model(2).to(self.device)
            optimizer = torch.optim.SGD(model.parameters(), lr = 0.00001, momentum = 0.9)

            for epoch in range(1, EPOCH + 1):
                train_one_epoch(model, optimizer, train_dataloader1, self.device, epoch, BATCH_SIZE, print_freq = 1)
                train_one_epoch(model, optimizer, train_dataloader2, self.device, epoch, BATCH_SIZE, print_freq = 1)
                train_one_epoch(model, optimizer, train_dataloader3, self.device, epoch, BATCH_SIZE, print_freq = 1)

            model.eval()

            if not os.path.exists("./model/"):
                os.makedirs("./model/")
            torch.save(model, "./model/bounding_box_narrow_model.pkl")

        train_three_fold_data(train_dataloader1, train_dataloader2, train_dataloader3, 1)
        train_three_fold_data(train_dataloader2, train_dataloader3, train_dataloader1, 2)
        train_three_fold_data(train_dataloader1, train_dataloader3, train_dataloader2, 3)
        # train_all_data()

    def predict_all_bounding_box_narrow_data(self):
        if self.bounding_box_narrow_data == []:
            self.get_bounding_box_narrow_data()

        def findBoundingBox(mask):
            mask = np.array(mask)
            pos = np.where(mask)

            points = []
            for y, x in zip(pos[0], pos[1]):
                points.append([x, y])

            result = []
            if len(points) > 0:
                rect = cv2.minAreaRect(np.array(points))
                result = cv2.boxPoints(rect)

            return np.array(result, int)

        if torch.cuda.is_available():    
            model = torch.load("./model/{}".format(narrow_data_model))
        else:
            model = torch.load("./model/{}".format(narrow_data_model), map_location=torch.device('cpu'))

        result = np.load("./predict/bounding_box_wider_data_predict.npz")

        model.eval()
       
        predict = []
        
        for index in range(len(self.bounding_box_narrow_data)):
            x1, y1, x2, y2 = result["predict"][index]
            image = self.bounding_box_narrow_data[index][y1:y2, x1:x2]
            origin_shape = image.shape
            image = cv2.resize(image, (narrow_data_training_size, narrow_data_training_size), interpolation=cv2.INTER_LINEAR).astype(np.float64) / 255
            output = model([torch.tensor(image.transpose((2, 0, 1))).float().to(self.device)])
            if len(output[0]["masks"]) == 0:
                predict.append([[0, 0], [0, 1], [1, 1], [1, 0]])
                continue
            
            image = output[0]["masks"][0].data.cpu().numpy().transpose((1, 2, 0))
            bestScoreImage = cv2.resize(image, (origin_shape[1], origin_shape[0]), interpolation=cv2.INTER_LINEAR)
            
            predictPoints = findBoundingBox(bestScoreImage > 0.5)
            predict.append(predictPoints if len(predictPoints) > 0 else [[0, 0], [0, 1], [1, 1], [1, 0]])          

        if not os.path.exists("./predict/"):
            os.makedirs("./predict/")

        np.savez("./predict/bounding_box_narrow_data_predict.npz", predict = predict, goundTruth = self.bounding_box_narrow_target)


    def predict_bounding_box_narrow_data(self, index):
        if self.bounding_box_narrow_data == []:
            self.get_bounding_box_narrow_data()

        bounding_box_wider_data_result = np.load("./predict/bounding_box_wider_data_predict.npz", allow_pickle = True)
        bounding_box_narrow_data_result = np.load("./predict/bounding_box_narrow_data_predict.npz", allow_pickle = True)

        x1, y1, x2, y2 = bounding_box_wider_data_result["predict"][index]
        image, target = self.bounding_box_narrow_data[index], self.bounding_box_narrow_target[index]
        drawImage = np.array(image[y1:y2, x1:x2])

        predictPoints = bounding_box_narrow_data_result["predict"][index]
        if len(predictPoints) > 0:
            cv2.line(drawImage, tuple(predictPoints[0]), tuple(predictPoints[1]), (255, 0, 0), 2)
            cv2.line(drawImage, tuple(predictPoints[1]), tuple(predictPoints[2]), (255, 0, 0), 2)
            cv2.line(drawImage, tuple(predictPoints[2]), tuple(predictPoints[3]), (255, 0, 0), 2)
            cv2.line(drawImage, tuple(predictPoints[3]), tuple(predictPoints[0]), (255, 0, 0), 2)

        x, y, width, height, angle = np.array(target, float)
        rect = (x, y), (width, height), angle
        groundTruthPoints = np.array(cv2.boxPoints(rect), int)
        cv2.line(drawImage, tuple(groundTruthPoints[0]), tuple(groundTruthPoints[1]), (0, 0, 255), 2)
        cv2.line(drawImage, tuple(groundTruthPoints[1]), tuple(groundTruthPoints[2]), (0, 0, 255), 2)
        cv2.line(drawImage, tuple(groundTruthPoints[2]), tuple(groundTruthPoints[3]), (0, 0, 255), 2)
        cv2.line(drawImage, tuple(groundTruthPoints[3]), tuple(groundTruthPoints[0]), (0, 0, 255), 2)
        cv2.imwrite(imageTempFolder + narrow_data_result_filename, drawImage)
        # cv2.imshow("narrow_data_image", cv2.resize(drawImage, (drawImage.shape[1] * 2, drawImage.shape[0] * 2), interpolation=cv2.INTER_LINEAR))
        # cv2.waitKey()  
        # cv2.destroyAllWindows() 

    ########################################################################################################################################################
    ########################################################### train_classifier_data ######################################################################
    ########################################################################################################################################################

    def train_classifier_data(self):
        if self.classifier_dataset1 == []:
            self.get_classifier_data()
            self.classifier_data_transfer()

        EPOCH = 100
        BATCH_SIZE = 4

        train_dataloader1 = torch.utils.data.DataLoader(self.classifier_dataset1, batch_size = BATCH_SIZE, shuffle = True, num_workers = 1)
        train_dataloader2 = torch.utils.data.DataLoader(self.classifier_dataset2, batch_size = BATCH_SIZE, shuffle = True, num_workers = 1)
        train_dataloader3 = torch.utils.data.DataLoader(self.classifier_dataset3, batch_size = BATCH_SIZE, shuffle = True, num_workers = 1)

        number_of_batch = len(train_dataloader1)
        number_of_data = len(self.classifier_dataset1)

        def train_one_epoch(train_dataloader, model, optimizer, loss_func):
            nonlocal correct_predict, total_batch_loss

            for step, (datas, targets) in enumerate(train_dataloader):

                output = model(datas.float().to(self.device))
                optimizer.zero_grad()
                loss = loss_func(output, targets.long().to(self.device))
                loss.backward()
                optimizer.step()

                _, predict = torch.max(torch.nn.functional.softmax(output, dim = 1), 1)
                correct_predict += (predict.data.cpu() == targets).sum()
                total_batch_loss += loss.data.cpu().numpy()

                print("\r", "Batch of Training: %.4f" % (((step + 1) / number_of_batch) * 100.), "%", " (loss = {})".format(loss), end=" ")
            
            print()

        def evaluate(train_dataloader, model, loss_func):
            correct_predict = 0
            total_batch_loss = 0
            
            for datas, targets in train_dataloader:

                output = model(datas.float().to(self.device))
                loss = loss_func(output, targets.long().to(self.device))

                _, predict = torch.max(torch.nn.functional.softmax(output, dim = 1), 1)
                correct_predict += (predict.data.cpu() == targets).sum()
                total_batch_loss += loss.data.cpu().numpy()

            print("\r", "Test Data: Accuarcy = {}, loss = {}".format(correct_predict / number_of_data, total_batch_loss / number_of_batch))

        def train_three_fold_data(dataloader1, dataloader2, dataloader3, nameIndex):
            nonlocal correct_predict, total_batch_loss

            model = torch.nn.Sequential(
                torchvision.models.resnet50(pretrained=True), 
                torch.nn.ReLU(),
                torch.nn.Linear(1000, 2)
            ).to(self.device)
            optimizer = torch.optim.SGD(model.parameters(), lr = 0.0001, momentum = 0.9, weight_decay=0.0005)
            loss_func = torch.nn.CrossEntropyLoss()

            for epoch in range(1, EPOCH + 1):
                print("Epoch: {}".format(epoch))

                correct_predict = 0
                total_batch_loss = 0

                train_one_epoch(dataloader1, model, optimizer, loss_func)
                train_one_epoch(dataloader2, model, optimizer, loss_func)
                evaluate(dataloader3, model, loss_func)

                print("\n Epoch of Training: %.4f" % ((epoch / EPOCH) * 100.), "%", " (loss = {}, accuracy = {}, epoch: {})\n".format(total_batch_loss / (number_of_batch * 2), correct_predict / (number_of_data * 2), epoch), end=" ")
                print("====================================================")

            if not os.path.exists("./model/"):
                os.makedirs("./model/")
            torch.save(model, "./model/classifier_model{}.pkl".format(nameIndex))

        def train_all_data():
            nonlocal correct_predict, total_batch_loss

            model = torch.nn.Sequential(
                torchvision.models.resnet50(pretrained=True), 
                torch.nn.ReLU(),
                torch.nn.Linear(1000, 2)
            ).to(self.device)
            optimizer = torch.optim.SGD(model.parameters(), lr = 0.0001, momentum = 0.9, weight_decay=0.0005)
            loss_func = torch.nn.CrossEntropyLoss()

            for epoch in range(1, EPOCH + 1):
                print("Epoch: {}".format(epoch))

                correct_predict = 0
                total_batch_loss = 0

                train_one_epoch(train_dataloader1, model, optimizer, loss_func)
                train_one_epoch(train_dataloader2, model, optimizer, loss_func)
                train_one_epoch(train_dataloader3, model, optimizer, loss_func)

                print("\n Epoch of Training: %.4f" % ((epoch / EPOCH) * 100.), "%", " (loss = {}, accuracy = {}, epoch: {})\n".format(total_batch_loss / (number_of_batch * 3), correct_predict / (number_of_data * 3), epoch), end=" ")
                print("====================================================")

            if not os.path.exists("./model/"):
                os.makedirs("./model/")
            torch.save(model, "./model/classifier_model.pkl")

        correct_predict, total_batch_loss = 0, 0
        train_three_fold_data(train_dataloader1, train_dataloader2, train_dataloader3, 1)
        train_three_fold_data(train_dataloader2, train_dataloader3, train_dataloader1, 2)
        train_three_fold_data(train_dataloader1, train_dataloader3, train_dataloader2, 3)

        # correct_predict, total_batch_loss = 0, 0
        # train_all_data()

    
    def predict_all_classifier_data(self):
        if self.classifier_data == []:
            self.get_classifier_data()

        if torch.cuda.is_available(): 
            model = torch.load("./model/{}".format(classifier_data_model))
        else:
            model = torch.load("./model/{}".format(classifier_data_model), map_location=torch.device('cpu'))

        result = np.load("./predict/bounding_box_wider_data_predict.npz", allow_pickle = True)

        predict = []
        grad_cam_image = []

        for index, image in enumerate(self.classifier_data):
            x1, y1, x2, y2 = result["predict"][index]
            image = image[y1:y2, x1:x2]
            image = cv2.resize(image, (classifier_data_training_size, classifier_data_training_size), interpolation=cv2.INTER_LINEAR).astype(np.float32) / 255

            output = model(torch.tensor(np.array([image.transpose((2, 0, 1))])).float().to(self.device))
            _, pre = torch.max(torch.nn.functional.softmax(output, dim = 1), 1)
            predict.append(pre.data.cpu()[0])

            target_layers = [model[0].layer4[-1]]
            input_tensor = torch.tensor(np.array([image.transpose((2, 0, 1))])).float().to(self.device)
            cam = GradCAM(model=model, target_layers=target_layers, use_cuda=torch.cuda.is_available())
            grayscale_cam = cam(input_tensor=input_tensor)
            grayscale_cam = grayscale_cam[0, :]
            visualization = show_cam_on_image(image, grayscale_cam, use_rgb=True)
            grad_cam_image.append(visualization)

        if not os.path.exists("./predict/"):
            os.makedirs("./predict/")

        np.savez("./predict/classifier.npz", label = np.array(["Fracture", "Normal"]), predict = predict, goundTruth = self.classifier_target, grad_cam_image = grad_cam_image)


    def predict_classifier_data(self, index):

        result = np.load("./predict/classifier.npz")

        label = result["label"]
        predict = result["predict"]
        goundTruth = result["goundTruth"]
        grad_cam_image = result["grad_cam_image"]

        # print("predict = {}, groundTruth = {}".format(label[predict[index]], label[goundTruth[index]]))

        red, green, blue = cv2.split(grad_cam_image[index])
        image = cv2.merge([blue, green, red])
        cv2.imwrite(imageTempFolder + grad_cam_result_filename, image)
        # cv2.imshow("classifier_data_image", grad_cam_image[index])
        # cv2.waitKey()  
        # cv2.destroyAllWindows() 

        return label[predict[index]], label[goundTruth[index]]


