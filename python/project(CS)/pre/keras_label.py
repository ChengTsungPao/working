import cv2
import numpy as np
from glob import glob
import matplotlib.pylab as plt
from keras import optimizers
from keras.models import Sequential
from keras.layers import Dense, Activation, Convolution2D, MaxPooling2D, Flatten
from sklearn.model_selection import train_test_split


def get_data(path):
    health = glob(path+"health/*.bmp")
    unhealth = glob(path+"unhealth/*.bmp")
    filename = health + unhealth
    X = []
    Y = np.array([[0., 1.] for _ in range(len(health))] + [[1., 0.] for _ in range(len(unhealth))])
    #Y = np.array([0. for _ in range(len(health))] + [1. for _ in range(len(unhealth))])
    for f in filename:
        X.append(np.array(cv2.imread(f),float)/255.)
    X = np.array(X)
    X.reshape(len(health) + len(unhealth), -1)
    return X, Y



path = "D:/program/vscode_workspace/private/data/project_image(CS)/"
X, Y = get_data(path)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, shuffle=True)

model = Sequential()
model.add(Convolution2D(batch_input_shape=(None, 511, 512, 3), filters=16, kernel_size=5, strides=1, padding='same',))
model.add(Activation('relu'))
model.add(MaxPooling2D(2))

model.add(Convolution2D(filters=32, kernel_size=5, strides=1, padding='same',))
model.add(Activation('relu'))
model.add(MaxPooling2D(2))

model.add(Flatten())
model.add(Dense(512))
model.add(Dense(2))
model.add(Activation('softmax'))

print(model.summary())

print('\nTraining ------------')
sgd = optimizers.SGD(lr=0.000001)
adam = optimizers.Adam(lr=0.000001)
model.compile(optimizer=adam, loss='categorical_crossentropy',  metrics=['accuracy'])
H = model.fit(X_train, Y_train, epochs=100, batch_size=16, validation_data=(X_test, Y_test), shuffle=True)

loss, accuracy = model.evaluate(X_test, Y_test)
print('\nTesting ------------')
print('test loss: ', loss)
print('test accuracy: ', accuracy)

plt.plot(range(len(H.history["loss"])), H.history["loss"], "o", label = "loss")
plt.plot(range(len(H.history["val_loss"])), H.history["val_loss"], "o", label = "val_loss")
plt.legend()
plt.show()
