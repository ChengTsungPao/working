from Corner_Detection import corner_detection
import cv2
import numpy as np

if __name__ == "__main__":

    problem = 1
    index = 1

    path = "..//Dataset_CvDl_Hw1//Q{}_Image//".format(problem)
    filename = "{}.bmp".format(index)

    image = cv2.imread(path + filename)
    # corner_detection(image)

    intrinsicMatrix, translations, rotations = corner_detection(path, False)
    print("#########################################################")
    print("intrinsic matrix = ")
    print(intrinsicMatrix)

    print(rotations)

    print("#########################################################")
    print("extrinsic matrix = ")
    extrinsicMatrix = [] 
    for i in range(len(translations)):
        extrinsicMatrix.append(np.concatenate((rotations[i], translations[i]), axis = 1))
        print(extrinsicMatrix[-1])
    extrinsicMatrix = np.array(extrinsicMatrix)



